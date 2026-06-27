# Mental Health Chatbot (AI Companion)

An empathetic AI chatbot built with Flask and OpenAI. The app listens to user messages, analyzes sentiment, and offers supportive responses and personalized suggestions.

## Features
- Sentiment analysis for mood detection
- Distress alert for crisis-related messages
- Empathetic responses via OpenAI
- Personalized self-care suggestions
- Simple Flask web interface

## Tech stack
- Python
- Flask
- OpenAI API
- HTML/CSS/JavaScript

## Setup
1. Create a project folder and navigate into it.
2. Copy `.env.example` to `.env` and set your `OPENAI_API_KEY`.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the app:
   ```bash
   python app.py
   ```
5. Open `http://127.0.0.1:5000` in your browser.

## Notes
- This project uses a lightweight rule-based sentiment analyzer for demonstration.
- For production use, add secure error handling, user authentication, logging, and crisis escalation flows.
