from flask import request, Blueprint, jsonify # pyright: ignore[reportMissingImports]
from ..schema.models import db, Users, Character
from ..constants.http_status_codes import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_201_CREATED
from ..services.AIgenerateStories import generate_bible_stories

chat_bp = Blueprint('character-chat', __name__, url_prefix='/api/character')

@chat_bp.route('/chat', methods=['POST'])
def chat_with_bible_character():

    character_id = 2

    user_id = 1
    # get the real user Id when the user logs in
    user = Users.query.filter_by(id=user_id).first()
    character = Character.query.filter_by(id=character_id).first()

    if not user:
        return jsonify({'error': 'User not found.'}), HTTP_404_NOT_FOUND
    

    conversation_history = [
        {
            "role": "system",
            "content": f"""{character.description}. You are a kind Bible character. You speak gently, friendly and wisely when asked questions. You do not respond to any questions outside of Biblical context. Your focus is on sharing the word of God to {user.username} in a narrative way and how God worked with you throughout your life and purpose. When greeted, you keep your introduction short and simple in one simple sentence. You ask follow up questions to know what the user wants to know.
            """
        }
    ]

    while True:
        user_message = request.json.get('message')
        if not user_message or user_message == '':
            return jsonify({'error': 'Input field should not be empty.'}), HTTP_400_BAD_REQUEST
    
        response, conversation_history = generate_bible_stories(user_message, conversation_history)

        return jsonify({'response': response}), HTTP_200_OK
        

