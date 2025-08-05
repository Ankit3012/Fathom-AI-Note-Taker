# Fathom-AI-Note-Taker
It is an AI Note-Taker like a Fathom made with Livekit and OpenAI
# 🎙️ LiveKit Multi-User Meeting Transcriber with GPT-4o Analysis

A production-ready Python voice agent using **LiveKit**, **Deepgram**, and **OpenAI GPT-4o** to transcribe multilingual conversations (English, Hindi, etc.) from multiple participants in real time and extract **structured meeting insights** such as:

- ✅ Call Summary  
- 🎯 Meeting Purpose  
- 📝 Key Points  
- 👤 User-Specific Tasks  
- 🔜 Next Steps  

## 🚀 Features

- 🎧 **LiveKit Audio Routing**: Real-time voice capture from multiple participants
- 🧠 **Deepgram STT**: Accurate multilingual transcription (supports English, Hindi, etc.)
- 🤖 **OpenAI GPT-4o**: Intelligent post-call analysis and summarization
- 📦 **PostgreSQL Integration**: Stores transcripts, summaries, and analysis in the DB
- 🔄 **Automatic Cleanup**: Call ends when all users disconnect, data is saved
- 🪄 **Speaker-Aware Labeling**: Recognizes and names participants intelligently

## 📂 Folder Structure

.
├── main.py # Main agent script (entrypoint)
├── db/
│ └── database.py # SQLAlchemy session setup
├── models/
│ └── models.py # NoteTakerCall model
├── .env # Environment variables
├── requirements.txt
└── README.md


## 🛠️ Tech Stack

| Tech        | Purpose                       |
|-------------|-------------------------------|
| [LiveKit](https://livekit.io/)     | WebRTC for real-time audio     |
| [Deepgram](https://deepgram.com/) | STT (Speech-to-Text)           |
| [OpenAI GPT-4o](https://openai.com/) | LLM for structured call insights |
| SQLAlchemy + PostgreSQL | Data storage                |

## 📥 Installation

---bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

# Setup virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

⚙️ Environment Variables (.env)
Create a .env file with:

env
Copy
Edit
OPENAI_API_KEY=your_openai_key
LIVEKIT_API_KEY=your_livekit_api_key
LIVEKIT_API_SECRET=your_livekit_secret
LIVEKIT_URL=your_livekit_url
DATABASE_URL=postgresql+psycopg2://user:pass@localhost:5432/yourdb
▶️ Running the Agent
bash
Copy
Edit
python main.py
This launches the note-taking agent using cli.run_app(). The agent listens to LiveKit events and starts transcription when participants join.

📊 Example Output
json
Copy
Edit
{
  "summary": "The team discussed progress on the backend and frontend tasks...",
  "purpose": "Sprint planning and task delegation",
  "key_points": [
    "Rahul completed backend integration",
    "Anjali will finalize the UI by Friday"
  ],
  "users_tasks": {
    "Rahul": ["Test and deploy backend service"],
    "Anjali": ["Finish UI design", "Push code to repo"]
  },
  "next_steps": ["Schedule next sync-up on Monday"]
}
📌 Note
Transcription and analysis only start after a participant speaks.

Once all participants disconnect, the final transcript is analyzed and stored in DB.

🙏 Acknowledgements
Built with ❤️ using LiveKit, Deepgram, and OpenAI.

💬 License
MIT — free to use and modify. Contributions welcome!





