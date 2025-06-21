from flask import request, Blueprint, jsonify # pyright: ignore[reportMissingImports]
from ..schema.models import db, Users
from ..constants.http_status_codes import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_201_CREATED
from ..services.AIgenerateStories import generate_bible_stories

story_bp = Blueprint('stories', __name__, url_prefix='/api/chat')

@story_bp.route('/read-stories', methods=['POST'])
def get_ai_stories():
    user_prompt = request.json.get('prompt')

    user_id = 1
    # get the real user Id when the user logs in
    user = Users.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({'error': 'User not found.'}), HTTP_404_NOT_FOUND
    
    if not user_prompt or user_prompt == '':
        return jsonify({'error': 'Input field should not be empty.'}), HTTP_400_BAD_REQUEST
    

    conversation_history = [
        {
            "role": "system",
            "content": f"""You are a friendly devoted christian, child-safe Holy Bible assistant named Biblia. You have been created as a friendly Bible companion to narrate Bible stories and change people's lives. Your introduction should be short and onpoint. You help and answer bible questions in simple, kind, and gentle language suitable for children aged 8-20. Refer to Bible teachings where relevant. You are also a good Bible story-teller who is able to narrate Bible stories based on what the user is feeling. You do not respond to any questions outside of Biblical context. Your focus is on sharing the word of God and narrate Bible contexts to the user, {user.username}. Try to ask follow-up questions to keep the conversation going.
            """
        }
    ]

    response, conversation_history = generate_bible_stories(user_prompt, conversation_history)

    return jsonify({'response': response}), HTTP_200_OK
        

