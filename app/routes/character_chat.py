from flask import request, Blueprint, jsonify # pyright: ignore[reportMissingImports]
from ..schema.models import db, Users, Character, Message, Conversation
from ..constants.http_status_codes import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_201_CREATED
from ..services.AIgenerateStories import generate_bible_stories
from flask_jwt_extended import jwt_required, get_jwt_identity # pyright: ignore[reportMissingImports]

chat_bp = Blueprint('character-chat', __name__, url_prefix='/api/character')

# character chat route
@chat_bp.route('/<character_id>/chat', methods=['POST'])
@jwt_required()
def chat_with_bible_character(character_id):
    # get character to chat with
    character = Character.query.filter_by(id=character_id).first()

    user_id = get_jwt_identity()
    # get the real user Id when the user logs in
    user = Users.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({'error': 'User not found.'}), HTTP_404_NOT_FOUND
    
    messages = [
        {
            "role": "system", "content": f"""{character.description}. You are a kind Bible character. You speak gently, friendly and wisely when asked questions. You do not respond to any questions outside of Biblical context. Your focus is to have a personal conversation with user: {user.username}, by sharing the word of God from the Holy Bible and how God worked with you throughout your life and purpose. When greeted, you keep your introduction short and simple in one simple sentence. When you are asked to pray, you pray in the name of Jesus Christ. You speak as a friend not too descriptive of what you are doing, just have a conversation not like a story. You ask follow up questions to keep the conversation going.
            """
        }
    ]

    while True:
        user_message = request.json.get('message')
        if not user_message or user_message == '':
            return jsonify({'error': 'Input field should not be empty.'}), HTTP_400_BAD_REQUEST
        
        conversation_id = 1

        db.session.add(Message(sender_id=user_id, content=user_message, role='user', character_id=character_id, conversation_id=conversation_id))
        db.session.commit()

        history = Message.query.filter_by(sender_id=user_id).order_by(Message.created_at).all()
        messages += [msg.to_dict() for msg in history]

        reply = generate_bible_stories(messages)
        db.session.add(Message(sender_id=user_id, role='assistant', content=reply, character_id=character_id, conversation_id=conversation_id))
        db.session.commit()

        conversation_history = Message.query.filter_by(sender_id=user_id).order_by(Message.created_at).all()

        conversation_history_dicts = [msg.to_dict() for msg in conversation_history]

        return jsonify({'response': conversation_history_dicts}), HTTP_200_OK
        
# delete message
@chat_bp.route('/chat/<int:message_id>', methods=['DELETE'])
@jwt_required()
def delete_massage_from_chat(message_id):
    user_id = get_jwt_identity()

    if request.method == 'DELETE':
        message = Message.query.filter_by(sender_id=user_id, id=message_id).first()
        if not message:
            return {'error': 'Message not found.'}
        
        db.session.delete(message)
        db.session.commit()

        return {}, HTTP_200_OK

# Delete chat
@chat_bp.route('/chat/<int:conversation_id>', methods=['DELETE'])
@jwt_required()
def delete_massage_from_chat(conversation_id):
    user_id = get_jwt_identity()

    if request.method == 'DELETE':
        try:
            db.session.query(Message).join(Conversation).filter(
            Message.sender_id == user_id,
            Conversation.id == conversation_id
            ).delete(synchronize_session=False)
            
        except Exception as e:
            db.session.rollback()
            print(f'error: {e}')

        return {}, HTTP_200_OK


