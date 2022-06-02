from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user_model

class Show:
    db = "exam_3_schema"
    def __init__(self, data):
        self.id = data["id"]
        self.title = data["title"]
        self.network = data["network"]
        self.release_date = data["release_date"]
        self.description = data["description"]              
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

        self.user = {}



    @staticmethod
    def validate_show(form_data):
        is_valid = True

        
       
        
        if len(form_data["title"]) < 3:
            flash("Title must be 3 characters long")
            is_valid = False

        if len(form_data["network"]) < 3:
            flash("Network must be 3 characters long")
            is_valid = False
               
        if len(form_data["release_date"]) <= 0:
            flash("Please enter a date year")
            is_valid = False
            
        if len(form_data["description"]) < 10:
            flash("Description must be 10 characters long")
            is_valid = False          
        
      
        return is_valid





    @classmethod
    def get_all_shows(cls):
        query = "SELECT * FROM shows LEFT JOIN users ON shows.user_id = users.id;"
        results = connectToMySQL(cls.db).query_db(query)
        user_all_shows = []
        for dict in results:
            user_shows = cls(dict)
            user_data = {
                'id' : dict['users.id'],
                'first_name' : dict["first_name"],
                'last_name' : dict["last_name"],
                'email' : dict["email"],
                'password' : dict["password"],
                'created_at' : dict["users.created_at"],
                'updated_at' : dict["users.updated_at"]
            }

            user_shows.user = user_model.User(user_data)
            user_all_shows.append(user_shows)

        return user_all_shows



    @classmethod
    def create_new_show(cls, data):
        query = "INSERT INTO shows (title, network, release_date, description, created_at, updated_at, user_id) VALUES (%(title)s, %(network)s, %(release_date)s, %(description)s, NOW(), NOW(), %(user_id)s);"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results



    @classmethod
    def delete_show(cls, data):
        query = "DELETE FROM shows WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results


    @classmethod
    def get_show_by_id(cls, data):
        query = "SELECT * FROM shows LEFT JOIN users ON shows.user_id = users.id WHERE shows.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        show = cls(results[0])
        user_data = {
            'id' : results[0]['users.id'],
            'first_name' : results[0]["first_name"],
            'last_name' : results[0]["last_name"],
            'email' : results[0]["email"],
            'password' : results[0]["password"],
            'created_at' : results[0]["users.created_at"],
            'updated_at' : results[0]["users.updated_at"]
        }

        show.user = user_model.User(user_data)
        
        return show
 

    @classmethod
    def edit_show(cls, data):
        query = "UPDATE shows SET title = %(title)s, network = %(network)s, release_date = %(release_date)s, description = %(description)s, updated_at = now() WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results