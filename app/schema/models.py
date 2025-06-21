from datetime import datetime
from flask_sqlalchemy import SQLAlchemy # pyright: ignore[reportMissingImports]

# initialise the database
db = SQLAlchemy()

# Users table
class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False, unique=True)
    email = db.Column(db.String(90), nullable=False, unique=True)
    password_hash = db.Column(db.Text, nullable=False)
    profile_pic_url = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    story = db.relationship('Story', backref='user', lazy=True)
    def __repr__(self) -> str:
        return f'Users>>>{self.id}'

# Messages table
class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False, index=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.id', ondelete="CASCADE"), nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(30), nullable=False, default='user')
    character_id = db.Column(db.Integer, db.ForeignKey('bible_characters.id', ondelete="CASCADE"), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    sender = db.relationship('User', backref='messages', lazy=True)
    conversation = db.relationship('Conversation', backref='messages', lazy=True)
    character = db.relationship('Character', backref='messages', lazy=True)
    def __repr__(self) -> str:
        return f'Message>>>{self.id}'

class Conversation(db.Model):
    __tablename__ = 'conversations'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    def __repr__(self) -> str:
        return f'Conversation>>>{self.id}'

class Character(db.Model):
    __tablename__ = 'bible_characters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    def __repr__(self) -> str:
        return f'Character>>>{self.id}'

class Story(db.Model):
    __tablename__ = 'bible_stories'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False, index=True)

    def __repr__(self) -> str:
        return f'Story>>>{self.id}'