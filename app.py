from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
from hugchat import hugchat
from hugchat.login import Login

app = Flask(__name__)
CORS(app)  # Enable CORS for the entire app

def get_chatbot():
    # Log in to HuggingChat with your credentials
    sign = Login("prahan", "Y4-LuY8iYzSKnGG")
    cookies = sign.login()
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
    return chatbot

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message')

    if user_message:
        # Initialize the chatbot and start a new conversation
        chatbot = get_chatbot()
        conversation_id = chatbot.new_conversation()
        chatbot.change_conversation(conversation_id)

        # Get the response from the chatbot
        bot_response = chatbot.chat(user_message)

        # Check if bot_response is a string or needs to be converted
        if isinstance(bot_response, str):
            response_message = bot_response
        else:
            # If it's not a string, extract the message content (assuming bot_response has a 'text' attribute)
            response_message = str(bot_response)  # Or extract specific attributes if necessary

        # Return the response from the chatbot
        response = {"response": response_message}
    else:
        response = {"response": "Sorry, I didn't understand that."}

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
