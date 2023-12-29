# Flask Backend for Sarcastic Email Response Generator

from flask import Flask, request, jsonify, render_template
import openai
import os


app = Flask(__name__)

# OpenAI API Key Setup
openai.api_key = os.environ.get("OPENAI_API_KEY")

client = openai.OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

def get_sarcastic_response(email_message):
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a sarcastic assistant."},
            {"role": "user", "content": email_message}
        ],
        model="gpt-3.5-turbo",
    )

    # Accessing the response
    latest_response = chat_completion.choices[0].message.content
    return latest_response

# Route to serve the HTML frontend
@app.route('/')
def index():
    return render_template('index.html')

# Endpoint to handle the API request
@app.route('/generate', methods=['POST'])
def generate():
    email_message = request.json.get('emailMessage')
    sarcastic_response = get_sarcastic_response(email_message)
    return jsonify({"response": sarcastic_response})

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
