from flask import Flask, render_template, request, jsonify
import requests

RASA_API_URL = 'http://localhost:5005/webhooks/rest/webhook'

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        user_message = request.json.get('message')
        if not user_message:
            return jsonify({'response': 'No message received.'}), 400

        rasa_response = requests.post(RASA_API_URL, json={'message': user_message})
        rasa_response_json = rasa_response.json()

        if not rasa_response_json:
            return jsonify({'response': 'No response from Rasa.'}), 500

        full_response = '\n\n'.join(r['text'] for r in rasa_response_json)
        return jsonify({'response': full_response})
    except Exception as e:
        return jsonify({'response': 'An error occurred: {}'.format(str(e))}), 500

if __name__ == "__main__":
    app.run(debug=True, port=3000)
