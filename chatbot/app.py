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
        # number of response
        n=3,
        # limit length of the response
        max_tokens = 100, 
        # controle the creativity, 0.2 is relatively small creativity = focused response,
        # 1.7 is high means more creativity on the topic, less focus
        temperature= 0.2, 
        # penalize AI for repeating words that were used in previous conversations, focus on conversations!!
        # 0.0 less penalty allowing AI to repeat more words freely
        # 1.0 high penalty encouraging the introduction of new topics, less repetition
        presence_penalty=0.8,
        # penalize AI for repeating words that were used in this same response,
        # 0.0 less penalty allowing AI to repeat more words freely
        # 1.0 high penalty encouraging the introduction of new topics, less repetition
        frequency_penalty=0.9,
        
    )
    
    # Extract the 3 responses
    replies = [choice.message.content.strip() for choice in response.choices]
    
    # Return as JSON
    return jsonify({"responses": replies})

if __name__ == "__main__":
    app.run(debug=True)
