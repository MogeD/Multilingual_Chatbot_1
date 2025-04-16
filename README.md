# Multilingual Regional Language Chatbot

A chatbot application that supports multiple regional languages, allowing users to have conversations in their preferred language.

## Features

- Support for multiple regional languages (currently Hindi and Telugu)
- Real-time language switching
- Modern, responsive UI
- Easy to extend for additional languages

## Project Structure

```
multilingual-chatbot/
├── backend/
│   ├── main.py          # FastAPI backend server
│   └── requirements.txt # Python dependencies
├── frontend/
│   ├── package.json    # Node.js dependencies
│   └── src/
│       └── App.js      # Main React component
└── README.md
```

## Setup Instructions

### Backend Setup

1. Create a Python virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install Python dependencies:

```bash
pip install -r requirements.txt
```

3. Start the backend server:

```bash
cd backend
uvicorn main:app --reload
```

The backend server will run on http://localhost:8000

### Frontend Setup

1. Install Node.js dependencies:

```bash
cd frontend
npm install
```

2. Start the frontend development server:

```bash
npm start
```

The frontend application will run on http://localhost:3000

## Usage

1. Open the application in your web browser at http://localhost:3000
2. Select your preferred language from the dropdown menu in the top-right corner
3. Type your message in the selected language
4. Press Enter or click the Send button to send your message
5. The chatbot will respond in the same language

## Supported Languages

Currently, the chatbot supports:

- Hindi (hi)
- Telugu (te)

To add support for additional languages, modify the `RESPONSES` dictionary in `backend/main.py` and add the corresponding language option in the frontend select menu.
