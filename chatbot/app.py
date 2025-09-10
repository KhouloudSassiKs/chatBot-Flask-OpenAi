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
client = OpenAI(api_key="YOUR_OPENAI_API_KEY")

# -----------------------
# Initial conversation setup
# -----------------------
conversation = [
    {"role": "user", "content": "Hello, chat bot at your service!"}  # initial message
]

def send_message(messages, n=1):
    """Helper to send messages to GPT-4 and return response(s)."""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        n=n,
        max_tokens=100,
        temperature=0.2,
        presence_penalty=0.8,
        frequency_penalty=0.9,
    )
    if n == 1:
        return response.choices[0].message.content.strip()
    return [choice.message.content.strip() for choice in response.choices]

# Get the first reply from GPT
initial_reply = send_message(conversation, n=1)
print("Assistant:", initial_reply)
conversation.append({"role": "assistant", "content": initial_reply})


# -----------------------
# Flask routes
# -----------------------

@app.route('/')
def index():
    # Pass the assistant’s initial reply into the template
    return render_template('index.html', initial_reply=initial_reply)


@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    # Add user message to conversation
    conversation.append({"role": "user", "content": user_message})

    # Get 3 different responses
    replies = send_message(conversation, n=3)

    # Save the first reply to conversation history (for continuity)
    conversation.append({"role": "assistant", "content": replies[0]})

    return jsonify({"responses": replies})


if __name__ == "__main__":
    app.run(debug=True)
