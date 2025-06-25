from datetime import datetime
from flask_sqlalchemy import SQLAlchemy # pyright: ignore[reportMissingImports]
import jwt 
from flask import current_app
from time import time
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
    
    def get_reset_password_token(self, expires_in=12213600):
        return jwt.encode({'reset_password': self.id, 'exp': time() + expires_in}, current_app.config['SECRET_KEY'], algorithm='HS256')
    
    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return
        return Users.query.get(id)

# Messages table
class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(30), nullable=False, default='user')
    character_id = db.Column(db.Integer, db.ForeignKey('bible_characters.id', ondelete="CASCADE"), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    sender = db.relationship('Users', backref='messages', lazy=True)
    character = db.relationship('Character', backref='messages', lazy=True)
    def __repr__(self) -> str:
        return f'Message>>>{self.id}'
    
    def to_dict(self):
        return {
            "role": self.role, 
            "content": self.content
        }

class Character(db.Model):
    __tablename__ = 'bible_characters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
    profile_image_url = db.Column(db.Text, nullable=True)
    book = db.Column(db.String(30), nullable=True)


    def __repr__(self) -> str:
        return f'Character>>>{self.id}'

class Story(db.Model):
    __tablename__ = 'bible_stories'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(30), nullable=False, default='user')
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False, index=True)

    def __repr__(self) -> str:
        return f'Story>>>{self.id}'
    def to_dict(self):
        return {
            "role": self.role,
            "content": self.content
        }