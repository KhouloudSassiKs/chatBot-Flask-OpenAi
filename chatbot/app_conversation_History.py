from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

# -----------------------
# Setup OpenAI client
# -----------------------
# Replace with your API key or set as an environment variable
client = OpenAI(api_key="YOUR_OPENAI_API_KEY")

# -----------------------
# Initial conversation setup
# -----------------------
conversation = [
    {"role": "user", "content": "Hello, chat bot at your service!"}
]

# -----------------------
# send_message function (single reply only)
# -----------------------
def send_message(messages, user_msg=None):
    """
    Sends a message to GPT-4, updates conversation history, and returns reply.

    Args:
        messages (list): Conversation history.
        user_msg (str, optional): User message to append before sending.

    Returns:
        str: Assistant's reply.
    """
    if user_msg:
        messages.append({"role": "user", "content": user_msg})

    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages
    )

    reply = response.choices[0].message.content.strip()
    messages.append({"role": "assistant", "content": reply})
    return reply

# -----------------------
# Demo conversation (bird facts)
# -----------------------
bird_conversation = []
send_message(bird_conversation, "Can you tell me a fun fact about birds?")
send_message(bird_conversation, "Follow up question: can you tell another fact")

# Optional: print demo conversation
for item in bird_conversation:
    print(f"{item['role'].capitalize()} : {item['content']}")

# -----------------------
# Regular chatbot initial message
# -----------------------
initial_reply = send_message(conversation)
print("Assistant (chatbot):", initial_reply)

# -----------------------
# Flask routes
# -----------------------
@app.route('/')
def index():
    return render_template('index.html', initial_reply=initial_reply)

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    # Get a single reply from GPT
    reply = send_message(conversation, user_msg=user_message)

    return jsonify({"response": reply})

if __name__ == "__main__":
    app.run(debug=True)
