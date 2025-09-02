from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)
# I can't share my personal api key here, you can get your own key:
# 1. login to your account
# 2. go to https://platform.openai.com/account/api-keys
# 3. OpenAi will generate a secret key for you
# 4. use your key and do not share it
client = OpenAI(api_key="YOUR_OPENAI_API_KEY")  
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message")
    
    # Request 3 responses from GPT-4
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": user_message}],
        n=3
    )
    
    # Extract the 3 responses
    replies = [choice.message.content.strip() for choice in response.choices]
    
    # Return as JSON
    return jsonify({"responses": replies})

if __name__ == "__main__":
    app.run(debug=True)
