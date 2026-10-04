# PodForge AI

> Turn your documents into engaging AI-powered podcasts.

PodForge AI is a full-stack AI application that transforms PDF documents into natural two-host podcast conversations.

Upload a PDF, let AI analyze the content and generate a conversational podcast script, then listen to the final podcast with two distinct AI-generated voices.

---

## ✨ Features

- 📄 Upload PDF documents
- 📝 Extract text automatically from PDFs
- 🤖 Generate podcast conversations using Google Gemini
- 🎙️ Generate conversations between two AI hosts
- 🔊 Generate distinct voices using Kokoro TTS
- ▶️ Play the generated podcast directly in the browser
- 📖 View the generated conversation transcript
- 📊 Display document statistics
- 🖱️ Drag-and-drop PDF upload
- 📱 Responsive web interface
- 🔐 Secure API key management using environment variables

---

## 🛠️ Tech Stack

### Frontend

- React
- Vite
- JavaScript
- CSS

### Backend

- Python
- FastAPI
- Uvicorn
- PyMuPDF

### AI

- Google Gemini API
- Kokoro Text-to-Speech

### Tools

- Git
- GitHub
- VS Code

---

## 🏗️ How It Works

React Frontend + Vite
        |
        | HTTP
        v
FastAPI Backend
        |
        +------------------+------------------+
        |                  |                  |
        v                  v                  v
     PyMuPDF           Gemini AI         Kokoro TTS
  PDF Extraction      Script Generation     AI Voices

### Processing Pipeline

PDF Upload
    ↓
PDF Text Extraction
    ↓
Text Cleaning
    ↓
Gemini AI
    ↓
Two-Host Podcast Script
    ↓
Speaker Separation
    ↓
Kokoro Text-to-Speech
    ↓
Generated Audio
    ↓
Browser Audio Player

---

## 📁 Project Structure

PodForge-AI/
│
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   │
│   └── services/
│       ├── ai_generator.py
│       ├── pdf_processor.py
│       ├── text_processor.py
│       └── tts_generator.py
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── App.css
│   │   ├── App.jsx
│   │   ├── index.css
│   │   └── main.jsx
│   │
│   ├── package.json
│   ├── package-lock.json
│   └── vite.config.js
│
├── .env.example
├── .gitignore
└── README.md

---

## 🚀 Getting Started

### Prerequisites

Make sure the following are installed:

- Python 3.11+
- Node.js
- npm
- Git
- A Google Gemini API key

### 1. Clone the Repository

    git clone https://github.com/Juhi-Bhamare/PodForge-AI.git
    cd PodForge-AI

### 2. Configure the Gemini API

Create a `.env` file in the project root.

Add:

    GEMINI_API_KEY=your_gemini_api_key_here

Your project should look like:

PodForge-AI/
├── .env
├── .env.example
├── backend/
└── frontend/

Never commit your actual API key to GitHub.

The `.env` file is excluded using `.gitignore`.

### 3. Set Up the Backend

Open a terminal in the project root:

    cd backend

Create a Python virtual environment:

    python -m venv venv

#### Windows PowerShell

Activate the environment:

    venv\Scripts\Activate.ps1

Install the required dependencies:

    pip install -r requirements.txt

Start the FastAPI development server:

    uvicorn main:app --reload

The backend will run at:

    http://127.0.0.1:8000

You can also check the API health endpoint:

    http://127.0.0.1:8000/health

### 4. Set Up the Frontend

Open a second terminal.

From the project root:

    cd frontend

Install the dependencies:

    npm install

Start the Vite development server:

    npm run dev

The frontend will run at:

    http://localhost:5173

Open that address in your browser.

---

## 🔑 Environment Variables

PodForge AI currently requires the following environment variable:

    GEMINI_API_KEY=your_gemini_api_key_here

The repository includes `.env.example` as a safe configuration template.

The real `.env` file is intentionally excluded from Git.

---

## 📡 API Endpoints

### Health Check

    GET /health

Returns:

    {
      "status": "healthy"
    }

### Upload PDF

    POST /upload-pdf

Accepts a PDF document and returns document information including:

- Filename
- Number of pages
- Word count
- Character count
- Text preview

### Generate Podcast

    POST /generate-podcast-audio

Accepts a PDF document and performs the complete podcast generation pipeline:

1. Extracts text from the PDF
2. Processes the extracted text
3. Sends the content to Gemini
4. Generates a two-host podcast script
5. Separates the dialogue by speaker
6. Generates distinct AI voices using Kokoro
7. Returns the generated podcast information and audio

---

## 🤖 AI Pipeline

PodForge AI uses multiple stages to transform a document into audio.

### 1. Document Processing

PyMuPDF extracts text from the uploaded PDF.

### 2. Text Processing

The extracted content is cleaned and prepared before being sent to the AI model.

### 3. Podcast Generation

Google Gemini transforms the document into an engaging conversation between two hosts.

The generated format uses:

    HOST 1: ...
    HOST 2: ...

This makes it possible to identify which voice should be used for each part of the conversation.

### 4. Voice Generation

Kokoro Text-to-Speech generates audio for each speaker.

The application currently uses different voices for the two hosts:

    HOST 1 → af_heart
    HOST 2 → am_adam

### 5. Audio Assembly

The generated speech segments are combined into a single podcast audio file.

---

## 🔒 Security

API credentials are never stored directly in the source code.

Local secrets are stored in:

    .env

A safe example configuration is provided through:

    .env.example

The repository's `.gitignore` prevents `.env` and other sensitive/local files from being committed.

---

## 📊 Current Capabilities

| Feature | Status |
|---|---|
| PDF upload | ✅ |
| PDF text extraction | ✅ |
| Text cleaning | ✅ |
| Gemini podcast generation | ✅ |
| Two-host conversation | ✅ |
| Two distinct AI voices | ✅ |
| Podcast audio generation | ✅ |
| Audio playback | ✅ |
| Transcript display | ✅ |
| Document statistics | ✅ |
| Drag-and-drop upload | ✅ |
| GitHub repository | ✅ |
| Public deployment | 🔄 Planned |

---

## 🔮 Future Improvements

Possible future improvements include:

- Support for additional document formats
- Custom podcast length
- Multiple voice options
- Custom host personalities
- Background music
- Sound effects
- Podcast download functionality
- Podcast generation history
- User authentication
- Cloud audio storage
- Improved processing for very large documents
- Public cloud deployment
- Streaming audio generation

---

## 🎯 Project Goals

PodForge AI was built to explore the practical use of generative AI in a full-stack application.

The project combines:

- Document processing
- Generative AI
- Text-to-speech
- REST APIs
- React frontend development
- Python backend development
- Environment-based secret management
- Git and GitHub

---

## 👨‍💻 Author

**Juhi-Bhamare**

GitHub:
https://github.com/Juhi-Bhamare

---

## 📄 License

This project is currently intended as a portfolio and learning project.