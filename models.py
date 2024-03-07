from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User (db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(24), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    messages = db.relationship('Message', backref='user')
    chats = db.relationship('Chat', backref = 'user')
    room = db.Column(db.Integer)
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
    def __repr__(self):
        return f'<User: {self.username}>'

class Message(db.Model):
    message_id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.chat_id'))
    text = db.Column(db.Text, nullable=False)

    def __init__(self, author_id, text, chat_id):
            self.author_id = author_id
            self.text = text
            self.chat_id = chat_id

    def __repr__(self):
            return '<Message {}'.format(self.chat_id)

class Chat (db.Model):
    chat_id = db.Column(db.Integer, primary_key = True)
    chat_name = db.Column(db.String(50))
    author_id = author_id = db.Column(db.Integer, db.ForeignKey('user.username'), nullable=False)
    messages = db.relationship('Message', backref='chat')
    
    def __init__(self, author_id, chat_name):
        self.author_id = author_id
        self.chat_name = chat_name
        def __repr__(self):
            return '<Chat {}'.format(self.chat_id)

