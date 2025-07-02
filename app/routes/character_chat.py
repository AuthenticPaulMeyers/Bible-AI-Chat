from flask import request, Blueprint, jsonify
from ..schema.models import db, Users, Character, Message
from ..constants.http_status_codes import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_201_CREATED
from ..services.AIgenerateStories import generate_bible_stories
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import limiter, get_remote_address
from ..utils.image_uploads import upload_image_to_supabase

chat_bp = Blueprint('character-chat', __name__, url_prefix='/api/v1.0.0/characters')

BOOKS = ['New Testament', 'Old Testament']

# character chat route
@chat_bp.route('/<int:character_id>/chat', methods=['POST'])
@limiter.limit("150 per day", key_func=get_remote_address)
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
            "role": "system", "content": f"""{character.description}. You are an assistant kind Bible character. You speak wisely with the Knowledge of God when asked questions. You do not respond to any questions outside of Biblical context. Your focus is to have a personal conversation with user: {user.username}, and how you can help the user's life by sharing the Word of God from the Holy Bible and how God worked with you throughout your life and purpose. When greeted, you keep your introduction short and simple in one line. When you are asked to pray, you pray in the name of Jesus Christ. Do not be descriptive just reply as a normal human being. You ask friendly questions to keep the conversation going.
            """
        }
    ]

    try:
        user_message = request.json.get('content')
        if not user_message or user_message == '':
            return jsonify({'error': 'Input field should not be empty.'}), HTTP_400_BAD_REQUEST

        db.session.add(Message(sender_id=user_id, content=user_message, role='user', character_id=character_id))
        db.session.commit()

        history = Message.query.filter_by(sender_id=user_id).order_by(Message.created_at).all()
        messages += [msg.to_dict() for msg in history]

        reply = generate_bible_stories(messages)

        reply = reply.replace("*", "")

        db.session.add(Message(sender_id=user_id, role='assistant', content=reply, character_id=character_id))
        db.session.commit()

        conversation_history = Message.query.filter_by(sender_id=user_id, character_id=character_id).order_by(Message.created_at).all()

        conversation_history_dicts = [msg.to_dict() for msg in conversation_history]

        return jsonify({'response': conversation_history_dicts}), HTTP_200_OK
    except Exception as e:
        print(f'Error: {e}')
    
# delete messages with the character
@chat_bp.route('/<int:character_id>/chat/<int:message_id>/delete', methods=['DELETE'])
@jwt_required()
def delete_massage_from_chat(message_id, character_id):
    user_id = get_jwt_identity()

    if request.method == 'DELETE':
        try:
            message = Message.query.filter_by(sender_id=user_id, id=message_id, character_id=character_id).first()
            if not message:
                return {'error': 'Message not found.'}
            
            db.session.delete(message)
            db.session.commit()

            conversation_history = Message.query.filter_by(sender_id=user_id).order_by(Message.created_at).all()

            conversation_history_dicts = [msg.to_dict() for msg in conversation_history]

            return jsonify({'response': conversation_history_dicts}), HTTP_200_OK
        
        except Exception as e:
            print(f'error: {e}')

# get messages with the character
@chat_bp.route('<int:character_id>/messages', methods=['GET'])
@jwt_required()
def get_messages(character_id):

    user_id = get_jwt_identity()
    if character_id:
        try:
            conversation_history = Message.query.filter_by(sender_id=user_id, character_id=character_id).order_by(Message.created_at).all()

            conversation_history_dicts = [msg.to_dict() for msg in conversation_history]
            return jsonify({'response': conversation_history_dicts}), HTTP_200_OK
        except Exception as e:
            print('Error:', e)
    return {'error': 'Chats not found.'}, HTTP_404_NOT_FOUND

# Delete/clear whole chat with character
@chat_bp.route('/<int:character_id>/chat/clear', methods=['DELETE'])
@jwt_required()
def delete_chat(character_id):
    user_id = get_jwt_identity()

    if request.method == 'DELETE':
        try: 
            chat = Message.query.filter_by(sender_id=user_id, character_id=character_id).all()
            if chat or chat != None:
                for msg in chat:
                    db.session.delete(msg)
                    db.session.commit()
                return {'message': 'Cleared chat successfully.'}, HTTP_200_OK
        except Exception as e:
            print(f'error: {e}')

# Display all characters with filter
@chat_bp.route('/get-all', methods=['GET', 'OPTIONS'])
@jwt_required()
def get_all_characters():

    filter_query = request.args.get('filter')
    if filter_query:
        filter_query = filter_query if filter_query else None

    if request.method == 'OPTIONS':
        return '', HTTP_200_OK
    
    query = Character.query

    if filter_query in BOOKS:
        query = query.filter_by(book = filter_query)
    
    results = query.all()

    print(filter_query)

    if not results:
        return jsonify({'error': 'Character not found.'}), HTTP_404_NOT_FOUND

    characters = []

    for character in results:
        characters.append({
            'id': character.id,
            'name': character.name,
            'description': character.description,
            'profile_image_url': character.profile_image_url,
            'book': character.book
        })
    return {'characters': characters}, HTTP_200_OK

# Add character
@chat_bp.route('/add', methods=['POST'])
@jwt_required()
def add_bible_character():
    name = request.form.get('name').capitalize().strip()
    description = request.form.get('description')
    char_book = request.form.get('book').strip().title()
    file = request.files.get('image')

    if not name or name == '' or not description or description == '' or not char_book or char_book == '':
        return jsonify({'error': 'Required fields should not be empty.'}), HTTP_400_BAD_REQUEST
    
    if char_book not in BOOKS:
        return jsonify({'error': 'Invalid book.'}), HTTP_400_BAD_REQUEST
    
    if not file:
        return jsonify({'error': 'No file provided.'}), HTTP_400_BAD_REQUEST
        
    file_url = upload_image_to_supabase(file)
    if not file_url:
        return jsonify({'error': 'Invalid file type.'}), HTTP_400_BAD_REQUEST

    if request.method == 'POST':
        try:
            db.session.add(Character(name=name, description=description, profile_image_url=file_url, book=char_book))
            db.session.commit()
            return jsonify({
                'message': 'Character created successfully.',
                'character':{
                    'name': name,
                    'description': description,
                    'book': char_book,
                    'profile_pic_url': file_url
                }
            }), HTTP_201_CREATED
        
        except Exception as e:
            print(f'error: {e}')

# Delete character
@chat_bp.route('/<int:character_id>/delete', methods=['DELETE'])
@jwt_required()
def delete_bible_character(character_id):

    if request.method == 'DELETE':
        try:
            character = Character.query.filter_by(id=character_id).first()
            db.session.delete(character)
            db.session.commit()
            return jsonify({'message': 'Character removed successfully.'}), HTTP_200_OK
        except Exception as e:
            print(f'error: {e}')

# Search character by name
@chat_bp.route('/search', methods=['GET'])
@jwt_required()
def search_character():
    get_name = request.args.get('name').capitalize().strip()

    if not get_name or get_name == '':
        return jsonify({'error': 'Missing required search query.'}), HTTP_400_BAD_REQUEST
    
    if request.method == 'GET':
        try:
            query = Character.query.filter_by(name=get_name).first()
            if not query:
                return jsonify({'error': 'No results found.'}), HTTP_404_NOT_FOUND
            return jsonify({
                'results':{
                    'id': query.id,
                    'name': query.name,
                    'profile_picture': query.profile_image_url,
                    'character_book': query.book
                }
            }), HTTP_200_OK
        # catch any other unexpected error
        except Exception as e:
            print(f'Unexpected error: {e}')
    