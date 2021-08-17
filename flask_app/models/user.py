from flask_app.config.mysqlcontroller import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    def __init__(self, data):
        self.id = data['id']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        users_from_db = connectToMySQL('users_db').query_db(query)
        users = []
        for user in users_from_db:
            users.append(cls(user))
        return users

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL("users_db").query_db(query, data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def save(cls, data):
        query = "Insert INTO users (email, password, created_at, updated_at) VALUES (%(email)s, %(password)s, NOW(), NOW());"
        return connectToMySQL('users_db').query_db(query, data)

    @staticmethod
    def validate_user(user):
        is_valid = True
        # test whether a field matches the pattern
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!")
            print("Invalid email address!")
            is_valid = False
        return is_valid

    @staticmethod
    def passwords_match(password, password2):
        match = True
        if password != password2:
            flash("Passwords don't match.")
            print("Passwords don't match.")
            match = False
            return match
        else:
            print("Passwords match!")
            return match
