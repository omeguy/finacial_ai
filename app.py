from flask import Flask, request, jsonify
from flask_cors import CORS
from finacial_ai.neuralintent.assistant import GenericAssistant

def custom_greeting():
    return "Hello, this is a custom response for greeting!"

def bye():
    return "goodbye!!!"

intent_methods = {
    "greetings": custom_greeting,
    "goodbye": bye
    # Add more entries if you have other intents to handle with custom methods
}

model_path = "./model"  # the directory where you saved your trained BERT model

# create assistant instance
assistant = GenericAssistant('intents.json', model_path, intent_methods)

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

@app.route('/chat', methods=['POST'])
def chat():
    message = request.json['message']
    response = assistant.get_response(message)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
