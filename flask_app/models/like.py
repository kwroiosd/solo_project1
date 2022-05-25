from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash



class Like():
    db = "app_ideas"
    def __init__(self,data):
        self.id = data['id']
        self.user_id = ['user_id']
        self.idea_id = ['idea_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
        
    @classmethod
    def save(cls,data):
        query = "INSERT INTO likes (user_id, idea_id) VALUES (%(user_id)s, %(idea_id)s);"
        print(data)
        return connectToMySQL(cls.db).query_db(query,data)  