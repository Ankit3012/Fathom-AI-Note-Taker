import asyncio, json, re
import logging, time
from dotenv import load_dotenv
from datetime import datetime
from livekit import rtc
from livekit.agents import (
    Agent,
    AgentSession,
    AutoSubscribe,
    JobContext,
    JobProcess,
    RoomInputOptions,
    RoomIO,
    RoomOutputOptions,
    StopResponse,
    WorkerOptions,
    cli,
    llm,
    utils,
)
from livekit.plugins import deepgram, silero
client = OpenAI()
# Your DB imports here
from db.database import SessionLocal
from models.models import NoteTakerCall

load_dotenv()

logger = logging.getLogger("transcriber")

class Transcriber(Agent):
    def __init__(self, *, participant_identity: str, transcript_collector: list):
        super().__init__(
            instructions="not-needed",
            stt=deepgram.STT(
                model="nova-3",
                language="multi",
                interim_results=True,
                punctuate=True,
                smart_format=True,
                numerals=True,
                sample_rate=16000,
                no_delay=True,
                endpointing_ms=25,
                filler_words=True,
                profanity_filter=False,
                mip_opt_out=True,
            ),
        )
        self.participant_identity = participant_identity
        self.transcript_collector = transcript_collector

    async def on_user_turn_completed(self, chat_ctx: llm.ChatContext, new_message: llm.ChatMessage):
        user_transcript = new_message.text_content
        logger.info(f"{self.participant_identity} -> {user_transcript}")
        self.transcript_collector.append(f"{self.participant_identity}: {user_transcript}")
        raise StopResponse()

async def analyze_chat(transcript_str: str) -> dict:
    """
    Analyze the plain-text chat transcript using OpenAI and return structured meeting insights.
    Accepts a raw transcript string with lines like 'identity-1234: message...'
    """
    prompt = """ 
You are an intelligent meeting assistant. Your task is to analyze a conference call transcript and return clear, structured insights, even if the conversation is informal, fragmented, or mixes English and Hindi.

Instructions:

1. Identify all speakers by name if mentioned (e.g., "My name is Rahul", "Hi Jack"). If the name is unclear, infer it from context (e.g., if someone is greeted by name) and label them with that name.
2. If no name is available, assign placeholder names like "Participant 1", "Participant 2", etc.
3. Extract all meaningful tasks or work discussed, even if briefly mentioned. Attribute each task to the correct person if possible.
4. If a participant mentions what they did or will do (e.g., "I worked on backend", "I'll submit frontend"), consider that a task.
5. Return a JSON object with:
   - summary: One paragraph summary
   - purpose: Meeting’s goal
   - key_points: List of important discussion points
   - users_tasks: Tasks for each user
   - next_steps: Actionable follow-ups
   - transcript_dict: Array of user-only messages in the same format as input (exclude assistant/agent/bot if any)

Be exhaustive and careful not to miss any tasks or actions, even if phrased casually. Preserve names as mentioned.

Transcript History:
"""

    try:
        response = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt + "\n" + transcript_str}],
                temperature=0.7,
            )
        )

        content = response.choices[0].message.content.strip()

        try:
            result = json.loads(content)
        except json.JSONDecodeError:
            match = re.search(r"
(?:json)?\s*(\{.*\})\s*
", content, re.DOTALL)
            if match:
                result = json.loads(match.group(1))
            else:
                raise ValueError("Response is not valid JSON")

        return result

    except Exception as e:
        logger.exception("❌ Chat analysis failed")
        return {}

    
class MultiUserTranscriber:
    def __init__(self, ctx: JobContext):
        self.ctx = ctx
        self._sessions: dict[str, AgentSession] = {}
        self._tasks: set[asyncio.Task] = set()
        self.transcript_data: list[str] = []
        self.participants_remaining: set[str] = set()

    def start(self):
        self.ctx.room.on("participant_connected", self.on_participant_connected)
        self.ctx.room.on("participant_disconnected", self.on_participant_disconnected)

    async def aclose(self):
        await utils.aio.cancel_and_wait(*self._tasks)
        await asyncio.gather(*[self._close_session(session) for session in self._sessions.values()])
        self.ctx.room.off("participant_connected", self.on_participant_connected)
        self.ctx.room.off("participant_disconnected", self.on_participant_disconnected)

        # Save final transcript to DB
        if self.transcript_data:
            logger.info("Enter...")
            combined_transcript = "\n".join(self.transcript_data)
            analysis = await analyze_chat(combined_transcript)
            logger.info(f"Transcript: {combined_transcript}")
            end_call_time=int(time.time() * 1000)
            db = SessionLocal()
            try:
              # NoteTakerCall is model tabel which store roomid, and notes with analysis and transcription with multilanguage using deepgram and openai
                note_call = db.query(NoteTakerCall).filter_by(call_id=self.ctx.room.name, call_status="active").first()
                if note_call:
                    note_call.call_status = "ended"
                    note_call.end_timestamp = end_call_time
                    note_call.call_analysis = analysis
                    note_call.duration_ms = end_call_time - note_call.start_timestamp
                    db.commit()
                    logger.info("✅ Transcript saved to DB")
            except Exception as e:
                logger.error(f"❌ Error saving transcript: {e}")
            finally:
                db.close()

    def on_participant_connected(self, participant: rtc.RemoteParticipant):
        if participant.identity in self._sessions:
            return

        logger.info(f"🟢 Connected: {participant.identity}")
        self.participants_remaining.add(participant.identity)
        task = asyncio.create_task(self._start_session(participant))
        self._tasks.add(task)

        def on_task_done(task: asyncio.Task):
            try:
                self._sessions[participant.identity] = task.result()
            finally:
                self._tasks.discard(task)

        task.add_done_callback(on_task_done)

    def on_participant_disconnected(self, participant: rtc.RemoteParticipant):
        if (session := self._sessions.pop(participant.identity)) is None:
            return

        logger.info(f"🔴 Disconnected: {participant.identity}")
        self.participants_remaining.discard(participant.identity)
        task = asyncio.create_task(self._close_session(session))
        self._tasks.add(task)
        task.add_done_callback(lambda _: self._tasks.discard(task))

        # If everyone disconnected, shutdown
        if not self.participants_remaining:
            asyncio.create_task(self.aclose())

    async def _start_session(self, participant: rtc.RemoteParticipant) -> AgentSession:
        if participant.identity in self._sessions:
            return self._sessions[participant.identity]

        session = AgentSession(vad=self.ctx.proc.userdata["vad"])
        room_io = RoomIO(
            agent_session=session,
            room=self.ctx.room,
            participant=participant,
            input_options=RoomInputOptions(text_enabled=False),
            output_options=RoomOutputOptions(transcription_enabled=True, audio_enabled=False),
        )
        await room_io.start()
        await session.start(agent=Transcriber(participant_identity=participant.identity, transcript_collector=self.transcript_data))
        return session

    async def _close_session(self, sess: AgentSession):
        await sess.drain()
        await sess.aclose()


async def entrypoint(ctx: JobContext):
    transcriber = MultiUserTranscriber(ctx)
    transcriber.start()

    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
    for participant in ctx.room.remote_participants.values():
        transcriber.on_participant_connected(participant)

    ctx.add_shutdown_callback(lambda: transcriber.aclose())


def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm, agent_name="note-taker-agent"))
