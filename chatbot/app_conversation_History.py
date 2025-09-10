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

# -----------------------
# Unified send_message function
# -----------------------
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Sends a message to GPT-4, updates conversation history, and returns reply(s).

Args:
messages (list): Conversation history.
user_msg (str, optional): User message to append before sending. Defaults to None.
n (int): Number of responses to request from GPT. Defaults to 1.

Returns:
   str or list: Assistant's reply or list of replies.
"""
def send_message(messages, user_msg=None, n=1):
    if user_msg:
        messages.append({"role": "user", "content": user_msg})

    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        n=n
    )

    if n == 1:
        reply = response.choices[0].message.content.strip()
        messages.append({"role": "assistant", "content": reply})
        return reply

    replies = [choice.message.content.strip() for choice in response.choices]
    messages.append({"role": "assistant", "content": replies[0]})
    return replies

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
    # Pass the assistant’s initial reply into the template
    return render_template('index.html', initial_reply=initial_reply)


@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    # Get 3 different responses from GPT
    replies = send_message(conversation, user_msg=user_message, n=3)

    return jsonify({"responses": replies})


if __name__ == "__main__":
    app.run(debug=True)
