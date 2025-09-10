from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

# Setup OpenAI client
# I can't share my personal api key here, you can get your own key:
# 1. Login to your account 
# 2. Go to https://platform.openai.com/account/api-keys 
# 3. OpenAi will generate a secret key for you 
# 4. Use your key and do not share it
client = OpenAI("OPENAI_API_KEY")

# -----------------------
# Routes
# -----------------------
@app.route('/')
def index():
    """Render the main chatbot interface (index.html)."""
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages from the frontend."""
    data = request.json
    user_message = data.get("message")
    temperature = data.get("temperature", 0.7)  # default creativity
    
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    # Request 3 responses from GPT-4
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": user_message}],
        n=3,  # number of responses
        max_tokens=100,  # response length limit
        temperature=temperature,  # AI creativity level
        presence_penalty=0.8,  # penalize repeated topics
        frequency_penalty=0.9,  # penalize repeated words
    )

    # Extract the 3 responses
    replies = [choice.message.content.strip() for choice in response.choices]

    # Return as JSON
    return jsonify({
        "responses": replies,
        "temperature_used": temperature
    })


# -----------------------
# Run App
# -----------------------
if __name__ == "__main__":
    app.run(debug=True)
