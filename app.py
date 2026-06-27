import os
import logging
from dotenv import load_dotenv

load_dotenv()

from flask import Flask, render_template, request, jsonify
from chatbot import generate_response
from sentiment import analyze_sentiment
from suggestions import build_suggestions

# Configure logging to show errors
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    # Don't crash the server on startup — return a clear error from the /chat endpoint instead.
    print("Warning: OPENAI_API_KEY is not set. Chat responses that require the OpenAI API will fail until it is configured.")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json or {}
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"error": "Please send a valid message."}), 400

    # If the OpenAI API key is missing, return a helpful error instead of crashing.
    if not openai_api_key:
        return jsonify({"error": "Server misconfiguration: OPENAI_API_KEY is missing. Please set it in .env or your environment."}), 500

    try:
        sentiment = analyze_sentiment(message)
        suggestions = build_suggestions(sentiment)
        response_text = generate_response(message, sentiment)

        result = {
            "reply": response_text,
            "sentiment": sentiment,
            "suggestions": suggestions,
        }
    except Exception as e:
        # Log the full error for debugging
        logger.error(f"Error in /chat endpoint: {str(e)}", exc_info=True)
        # Return JSON error for the frontend to display and avoid leaving the UI in a "Thinking..." state.
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

    if sentiment["distress_alert"]:
        result["alert"] = (
            "It sounds like you are going through a difficult time. "
            "If you are in immediate danger or feeling unsafe, please contact local emergency services or a trusted person right away."
        )

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
