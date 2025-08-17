# 📝 Fathom AI Note Taker (Open Source Alternative)

An **open-source AI note-taker** inspired by **Fathom**, built with **LiveKit**, **Deepgram**, and **OpenAI GPT-4o**.  
It transcribes multilingual conversations (English, Hindi, etc.) in **real time**, generates meeting summaries, and extracts **structured insights** such as:

- ✅ Call Summaries  
- 🎯 Meeting Purpose  
- 📝 Key Discussion Points  
- 👤 Action Items & Tasks per User  
- 🔜 Next Steps & Follow-ups  

---

## 🚀 Why Use This Project?

If you’ve used **Fathom AI Notetaker**, this is a **self-hosted alternative** you can run on your own infrastructure.  
Perfect for **remote teams, online meetings, classrooms, and customer calls**.  

Key benefits:  
- 🔓 100% Open Source — your data stays with you  
- 🌍 Multilingual transcription (English, Hindi, more)  
- ⚡ Real-time & speaker-aware analysis  
- 🗄️ PostgreSQL storage for transcripts and summaries  

---

## 🛠️ Features

- 🎧 **LiveKit Audio Routing** → Capture real-time audio from multiple participants  
- 🧠 **Deepgram STT** → Accurate speech-to-text in multiple languages  
- 🤖 **OpenAI GPT-4o** → AI-powered summarization, insights, and action items  
- 🪄 **Speaker-Aware Labeling** → Distinguishes between participants  
- 📦 **PostgreSQL + SQLAlchemy** → Persistent transcript & summary storage  
- 🔄 **Automatic Cleanup** → Ends session & saves data when all users disconnect  

---

## 📂 Project Structure

.
├── main.py # Entrypoint agent script
├── db/
│ └── database.py # SQLAlchemy session setup
├── models/
│ └── models.py # NoteTakerCall model
├── .env # Environment variables
├── requirements.txt # Python dependencies
└── README.md

yaml
Copy
Edit

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| [LiveKit](https://livekit.io/) | WebRTC audio capture & streaming |
| [Deepgram](https://deepgram.com/) | Speech-to-Text (STT) engine |
| [OpenAI GPT-4o](https://openai.com/) | AI insights & summarization |
| SQLAlchemy + PostgreSQL | Database storage |

---

## 📥 Installation Guide

```bash
# Clone the repo
git clone <your-repo-url>
cd Fathom-AI-Note-Taker

# Setup virtual environment
python -m venv venv
source venv/bin/activate   # (or venv\Scripts\activate on Windows)

# Install dependencies
pip install -r requirements.txt
⚙️ Environment Variables
Create a .env file:

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
This will:

Connect to LiveKit

Start real-time transcription

Run GPT-4o analysis

Save results in PostgreSQL

📊 Example Output
json
Copy
Edit
{
  "summary": "The team discussed progress on backend and frontend tasks...",
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
📌 Notes
Transcription starts when participants speak

Final transcript + summary is stored after call ends

Works with multiple users & languages

🙏 Acknowledgements
Built with ❤️ using LiveKit, Deepgram, and OpenAI GPT-4o.

💬 License
MIT — free to use, modify, and contribute.

🔎 Keywords (SEO)
AI Note Taker · Fathom AI Alternative · Open Source Meeting Transcriber · AI Meeting Assistant · LiveKit Transcription · Deepgram Speech to Text · OpenAI GPT-4o Summarization · Multilingual AI Notetaker · Self-hosted AI Notetaker

yaml
Copy
Edit

---

### 🔑 SEO Improvements I Added
- Keywords like **Fathom alternative**, **AI Notetaker**, **Meeting Transcriber**, **Multilingual**, etc.  
- Added **Why Use This Project?** section (helps both humans & search engines).  
- Inserted **keywords list at bottom** (SEO metadata hack).  
- Made **headings keyword-rich** (Google indexes them more heavily).  

---

👉 Do you want me to also create a **short project description (140–160 chars)** optimized for GitHub’s *About section* (this also improves Google ranking)?








Ask ChatGPT
