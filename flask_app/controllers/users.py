from flask import redirect, render_template, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.idea import Idea
from flask_app.models.like import Like
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/register',methods=['POST'])
def register():
    if not User.validate_user(request.form):
        return redirect('/')
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(data)
    session['user_id'] = id

    return redirect('/dashboard')

@app.route('/login',methods=['POST'])
def login():
    user = User.get_by_email(request.form)

    if not user:
        flash("Invalid Email","login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/dashboard')


@app.route('/dashboard')
def dashboard():
    #checking to make sure user is in session to enhance security
    if 'user_id' not in session:
        return redirect('/')
        #bringing in data of who is logged in
    data = {
        "id": session['user_id']
    }

    return render_template("dashboard.html",user=User.get_by_id(data),ideas=Idea.get_all_ideas_with_creator())

@app.route('/show/user/<int:id>')
def show_user(id):

    data = {
        "id":id
    }
    return render_template("user.html",user=User.get_by_id(data), idea=Idea.count_ideas(data))

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# @app.route('/like', methods=['GET', 'POST'])
# def like_post():
#     if 'user_id' not in session:
#         return redirect('/logout')

#     data = {
#         "user_id": session["user_id"],
#         "idea_id": ["idea_id"]
#     }
#     Like.save(data)
    
    
#     return redirect('/dashboard')