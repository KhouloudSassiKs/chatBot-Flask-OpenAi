from openai import OpenAI

# -----------------------
# Initialize OpenAI client
# -----------------------
# Setup OpenAI client
# I can't share my personal api key here, you can get your own key:
# 1. Login to your account 
# 2. Go to https://platform.openai.com/account/api-keys 
# 3. OpenAi will generate a secret key for you 
# 4. Use your key and do not share it
client = OpenAI("OPENAI_API_KEY")
# -----------------------
# Helper function
# -----------------------
"""
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
