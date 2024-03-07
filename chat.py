import os
import json
from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from models import User, db, Message, Chat

app = Flask(__name__)

app.config.update(dict(
	DEBUG=True,
	SECRET_KEY='secretkey',
	USERNAME='admin',
	PASSWORD='default',
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(app.root_path, 'chat.db')
))

db.init_app(app)

@app.cli.command('initdb')
def initdb_command():
	db.create_all()

@app.route('/', methods = ['GET','POST'])
def index():
    return render_template('logincreate.html')

@app.route('/create', methods = ['GET', 'POST'])
def create():
    if(request.method == 'POST'):
        username= request.form['user']
        if (User.query.filter_by(username=username).count()>0): #check to see if username exists
            return render_template('create.html')
        else:
            a = User(username = request.form['user'], password = request.form['pass']) #create the new user with given credentials and add to database
            db.session.add(a)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('createaccount.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if('username' in session):
        return redirect(url_for('lobby'))
    if (request.method == 'POST'):
        user1 = request.form['user']
        pass1 = request.form['pass']
        user = User.query.filter_by(username=user1).first()

        if(user is None): #user with given username does not exist
            return redirect(url_for('login'))
        session['username'] = user1
        return redirect(url_for('lobby'))
    return render_template('login.html')

@app.route('/logout',methods = ['GET', 'POST'])
def logout():
    if 'username' in session:
        session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/lobby',methods = ['GET', 'POST'])
def lobby():
    user = User.query.filter_by(username=session['username']).first()
    user.room = None
    db.session.commit()
    if(request.method == 'POST'):
        return redirect(url_for('createchat'))
    chats = Chat.query.all()
    return render_template('lobby.html', chats = chats, username = session['username'])

@app.route('/createchat', methods = ['GET', 'POST'])
def createchat():
    if(request.method == 'POST'):
        newchat = Chat(author_id = session['username'],chat_name = request.form['chatroom-name'])
        db.session.add(newchat)
        db.session.commit()
        return redirect(url_for('lobby'))
    return render_template('createchat.html')

@app.route('/deletechat/<int:chat_id>', methods = ['GET', 'POST'])
def delete(chat_id):
    if(request.method == 'GET'):
        chat = Chat.query.get_or_404(chat_id) #get the chat from database and delete it
        if(chat):
            db.session.delete(chat)
            db.session.commit()
    return redirect(url_for('lobby'))

@app.route('/chat/<int:chat_id>')
def chat(chat_id):
    user = User.query.filter_by(username=session['username']).first()
    if(user.room == None):
        user.room = chat_id
        db.session.commit()
    elif(user.room != chat_id):
        return redirect(url_for('chat', chat_id = user.room))

    chat_id_list = Chat.query.filter_by(chat_id = chat_id).all()
    if (chat_id not in [id.chat_id for id in chat_id_list]):
        flash("Chatroom has been deleted. Redirecting you to lobby.")
        return redirect(url_for('lobby'))
    messages = Message.query.filter_by(chat_id = chat_id)

    return render_template('chat.html', messages = messages)

@app.route("/new_message/<int:chat_id>", methods=["POST"])
def add(chat_id):
        messagetext = request.form.get("message")
        message = Message(author_id = session['username'],text = messagetext, chat_id = chat_id)
        db.session.add(message)
        db.session.commit()
        messages = Message.query.filter_by(chat_id = chat_id)
        records = [serialize_message(m) for m in messages]
        return json.dumps(records)     
    
@app.route("/messages/<int:chat_id>")
def get_messages(chat_id):
    chat_id_list = Chat.query.filter_by(chat_id = chat_id).all()
    if (chat_id not in [chat_id_list[0].chat_id for id in chat_id_list]):
        return redirect(url_for('lobby'))
    messages = Message.query.filter_by(chat_id = chat_id)
    records = [serialize_message(message) for message in messages]
    return json.dumps(records)  

def serialize_message(msg):
    return {
        "chat_id": msg.chat_id,
        "text": msg.text,
        "author_id": msg.author_id,
        "message_id": msg.message_id
    }

if __name__ == "__main__":
	app.run(debug=True)