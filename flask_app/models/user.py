from flask_app.config.mysqlconnection import connectToMySQL
import re 
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
from flask import flash
from flask_app.models import idea

class User():
    db = "app_ideas"
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.ideas = []


        
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
        

    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db).query_db(query)
        users = []
        for row in results:
            users.append( cls(row))
        return users


    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM users WHERE id = user_id;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        print(results)
        return cls(results[0])

    @classmethod
    def get_by_idea(cls, data):
        query = "SELECT * FROM ideas LEFT JOIN users ON ideas.user_id = users.id WHERE ideas.id = (user_id)"
        results = connectToMySQL(cls.db).query_db(query,data)
        users = cls( results[0] )
        for row in results:
            users.append( cls(row))
        print(results)
        return users
        

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @staticmethod
    def validate_user(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.db).query_db(query,user)
        # test whether a field matches the pattern
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", "register")
            print("yes")
            is_valid = False
        if len(results) >= 1:
            flash("Email in use by another client.", "register")
            is_valid = False
        if len(user['first_name']) < 2:
            flash("First Name must be at least 2 characters", "register")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last Name must be at least 2 characters", "register")
            is_valid = False
        if len(user['password']) < 3:
            flash("Password must be at least 8 characters", "register")
        if user['password'] != user['confirm_password']:
            flash("Passwords must match", "register")
            is_valid = False
        return is_valid