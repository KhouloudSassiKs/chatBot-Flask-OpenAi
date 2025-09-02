from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)
client = OpenAI(api_key="YOUR_OPENAI_API_KEY")  # Or use environment variable

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message")
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": user_message}]
    )
    reply = response.choices[0].message.content.strip()
    
    return jsonify({"response": reply})

if __name__ == "__main__":
    app.run(debug=True)
