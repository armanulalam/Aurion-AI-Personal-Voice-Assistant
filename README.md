# Aurion — Personal AI Voice Assistant

Aurion is a fully functional voice-controlled AI assistant built using Python.
It listens to voice commands, speaks responses, fetches information, manages tasks, sets alarms/reminders, sends emails/WhatsApp messages, retrieves news, plays music, and much more — all hands-free. Moreover, this project converted to .exe file.

This project integrates speech recognition, text-to-speech, Google Gemini AI, automations, and system interaction to create a smart desktop assistant.
The video demo of this project here https://youtu.be/CMGtA0AO0j4?si=ceIGl5wff7PgSsO8

## 🚀 Features
### 🎤 Voice Interaction

- Converts speech to text using speech_recognition

- Natural voice responses via pyttsx3

- Continuous listening loop

### 🧠 AI-Powered Responses

- Uses Google Gemini 2.5 Flash model for intelligent replies

- Generates short, concise answers

- Used for summarizing news and general questions

### 🗓️ Schedule Management

- Add tasks to daily schedule

- Read schedule aloud

- Clear schedule for the day

### 📝 To-Do List

- Add tasks via voice

- Show to-do list on console

- Delete a specific task (fuzzy matching included)

- Clear all tasks

### ⏰ Alarms & Reminders

- Set reminders with custom messages

- Set alarms in HH:MM format

- Automatically checks upcoming alarms/reminders

- Built-in beep sound for alarms

### 📰 Latest News Reader

- Fetches live news using NewsAPI

- Summarizes headlines using Gemini AI

- Reads out summaries aloud

### 🎵 Music Player

- Randomly plays songs from your music folder

- Announces the selected song

### 🌐 Web & App Shortcuts

- Open Google, YouTube, Notepad, Calculator, Calendar

- Search queries directly on YouTube

### 😄 Entertainment

- Reads jokes from a local jokes.txt file

### 📧 Email Sender

- Send emails via Gmail SMTP

- Uses saved contacts

- Requires an app password for secure login

### 💬 WhatsApp Messaging

- Send WhatsApp messages to:

- Individual contacts

- Groups

- Auto-detection of contact type (group/individual)

### 🛠️ Error Logging

- Stores all logs in a logs/application.log file

- Helpful for debugging voice recognition issues

## Tech Stack:

| Purpose            | Library               |
| ------------------ | --------------------- |
| Text-to-Speech     | `pyttsx3`             |
| Speech Recognition | `speech_recognition`  |
| AI Response        | `google-generativeai` |
| Web Automation     | `webbrowser`          |
| Wikipedia Search   | `wikipedia`           |
| WhatsApp Messaging | `pywhatkit`           |
| Email Sending      | `smtplib`             |
| News Fetching      | `requests`            |
| Task Matching      | `difflib`             |
| Logging            | `logging`             |

## ⚙️ Setup & Installation
1. Clone the Repository

```bash
git clone https://github.com/yourusername/Aurion-Voice-Assistant.git

cd Aurion-Voice-Assistant
```

2. Install Dependencies

```bash
pip install -r requirements.txt
```

3. Add API Keys

Inside the script, replace:

- GOOGLE_API_KEY

- NEWS_API_KEY

- EmailAppPass

with your real credentials.

4. Run the Assistant

```bash
python main.py
```

## 📌 Future Improvements

- GUI dashboard

- More offline capabilities

- Better NLP command detection

- Wake word activation (“Hey Aurion”)

- Custom dataset training

## 🤝 Contributing

Pull requests and feature suggestions are welcome!
Feel free to fork and enhance the assistant.
