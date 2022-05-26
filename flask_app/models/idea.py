from setuptools import find_namespace_packages
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user
from flask_app.models import like

class Idea():
    db = "app_ideas"
    def __init__(self,data):
        self.id = data['id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = ['user_id']
        self.occrances = []
        self.creator = None

        self.user = []

    @classmethod
    def save(cls,data):
        query = "INSERT INTO ideas (content, user_id) VALUES (%(content)s, %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def update(cls, data):
        query = "UPDATE ideas SET content=%(content)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM ideas WHERE ideas.id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_all(cls, data): 
        query = "SELECT * FROM ideas;"
        results = connectToMySQL(cls.db).query_db(query, data)
        data = {
            
        }        
        all_ideas = []
        for row in results:
            all_ideas.append( cls(row) )
        print(all_ideas)
        return all_ideas

    @classmethod
    def get_one_with_user(cls,data):
        query = "SELECT * FROM users LEFT JOIN ideas ON users.id = ideas.user_id WHERE ideas.user_id = users.id;"
        results = connectToMySQL(cls.db).query_db(query,data)
        ideas = cls( results[0] )
        for row in results:
            ideas.append( cls(row) )
        print(ideas)
        return results

    @classmethod
    def get_idea_with_user( cls , data ):
        query = "SELECT * FROM ideas LEFT JOIN users ON ideas.user_id = users.id WHERE ideas.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        one_idea = []
    
        idea = cls( results[0] )
        for row in results:
            
            user_data = {
                "id" : row["users.id"],
                "first_name" : row["first_name"],
                "last_name" : row["last_name"],
                "email" : row["email"],
                "password" : row["password"],
                "created_at" : row["users.created_at"],
                "updated_at" : row["users.updated_at"],
                "user_id" : ["user_id"]
            }
            idea.user.append( user.User( user_data ) )
        print(user_data["first_name"])
        return one_idea
        
    @classmethod
    def get_all_ideas_with_creator(cls):
        query = "SELECT * FROM ideas JOIN users ON ideas.user_id = (users.id);"
        results = connectToMySQL(cls.db).query_db(query)
        all_ideas = []
        
        for row in results:
            one_idea = cls(row)
            one_ideas_poster_info = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            poster = user.User(one_ideas_poster_info)
            one_idea.creator = poster
            all_ideas.append(one_idea)
        print(one_idea.creator.first_name)
        print(one_idea.creator.id)
        return all_ideas

        

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM ideas WHERE ideas.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        print(results)
        return cls(results[0])
        

    @classmethod
    def count_ideas(cls, data):
        query = "SELECT count(*) AS total_ideas FROM ideas WHERE user_id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        

        print(results[0])
        return (results[0])



    @staticmethod
    def validate_idea(idea):
        is_valid = True
        if len(idea['new_idea']) < 10:
            is_valid = False
            flash("Content must be at least 10 charachters.","idea")
        return is_valid