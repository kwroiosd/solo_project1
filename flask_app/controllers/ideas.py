from flask import render_template, session,flash,redirect, request
from flask_app import app
from flask_app.models.user import User
from flask_app.models.idea import Idea
from flask_app.models.like import Like

@app.route('/new/post', methods=['GET','POST'])
def create_post():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Idea.validate_idea(request.form):
        return redirect('/dashboard')
    data = {
        
        "content": request.form["new_idea"],
        "user_id": session["user_id"]
    }
    Idea.save(data)
    return redirect('/dashboard')

@app.route('/edit/idea/<int:id>')
def edit_idea(id):
    # if 'user_id' not in session:
    #     return redirect('/logout')
    # if not Idea.validate_idea(request.form):
    #     return redirect('/dashboard')
    data = {
        "id": id
    }
    user_data = {
        "id": session['user_id']
    }
    Idea.update(data)
    return render_template("edit_idea.html",edit=Idea.get_by_id(data),user=User.get_by_id(user_data))

@app.route('/update/idea', methods=['GET','POST'])
def update_idea():
    # if 'user_id' not in session:
    #     return redirect('/logout')
    if not Idea.validate_idea(request.form):
        return redirect('/dashboard')
    data = {
        "content": request.form['new_idea'],
        "id": request.form['id']
    }
    Idea.update(data)
    return redirect('/dashboard')

@app.route('/view/idea/<int:id>', methods = ['GET', 'POST'])
def show_idea(id):

    data = {
        "id": id 
    }
    user_data = {
        "id": session['user_id']
    }
    return render_template("idea.html",idea=Idea.get_all_ideas_with_creator(),user=User.get_by_id(user_data))

@app.route('/destroy/idea/<int:id>')
def destroy_idea(id):
    data = {
        "id": id
    }
    Idea.destroy(data)
    return redirect('/dashboard')
