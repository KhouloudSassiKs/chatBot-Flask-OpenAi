import uuid
from openai import OpenAI

# Store all active chat sessions
chat_sessions = {}

# Define a common system prompt for all conversations
system_prompt = {
    "role": "system",
    "content": (
        "You are an informed zookeeper, ready to assist children with their questions "
        "about animals and the zoo."
    )
}

# Function to create a new chat session
def create_chat():
    chat_id = str(uuid.uuid4())  # Generate a unique session identifier
    chat_sessions[chat_id] = [system_prompt.copy()]  # Initialize conversation with system prompt
    return chat_id

# Initialize OpenAI client
client = OpenAI()

# Function to send a message in a chat session
def send_message(chat_id, user_msg):
    if chat_id not in chat_sessions:
        raise ValueError("Chat session not found.")

    chat_sessions[chat_id].append({"role": "user", "content": user_msg})
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=chat_sessions[chat_id]
    )

    answer = response.choices[0].message.content.strip()
    chat_sessions[chat_id].append({"role": "assistant", "content": answer})
    return answer

# Example usage
if __name__ == "__main__":
    chat_id1 = create_chat()
    print("chat1 msg1:", send_message(chat_id1, "What are the best things about tigers?"))
    print("chat1 msg2:", send_message(chat_id1, "How about cheetahs?"))
