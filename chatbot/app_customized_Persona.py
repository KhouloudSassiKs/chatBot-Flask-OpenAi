from openai import OpenAI

# -----------------------
# Initialize OpenAI client
# -----------------------
# Make sure to set your API key in an environment variable or replace below
client = OpenAI(api_key="YOUR_OPENAI_API_KEY")

# -----------------------
# Helper function
# -----------------------
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Send a conversation history to GPT-4 and return the assistant's reply.

Args:
    messages (list): List of messages in the format [{"role": ..., "content": ...}]

Returns:
    str: Assistant's response
"""
def send_message(messages):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages
    )
    return response.choices[0].message.content.strip()


# -----------------------
# System persona setup
# -----------------------
system_prompt = "You are a cheerful chef who loves Tunisian food"

conversation = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": "What's your favorite type of pizza?"},
]

# -----------------------
# Request AI response
# -----------------------
reply = send_message(conversation)

# -----------------------
# Output
# -----------------------
print("Response:", reply)
