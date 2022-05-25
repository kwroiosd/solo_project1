from flask import render_template, session,flash,redirect, request
from flask_app import app
from flask_app.models import User
from flask_app.models import Idea
from flask_app.models import Like

@app.route('/like/<int:id>', methods=['GET', 'POST'])
def like_post(id):
    if 'user_id' not in session:
        return redirect('/logout')

    data = {
        "id": id,
        "user_id": session["user_id"]
    }
    Like.save(data)
    return redirect('/dashboard')