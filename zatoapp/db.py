import bson
import uuid
import time
from flask import current_app, g
from werkzeug.local import LocalProxy
from flask_pymongo import PyMongo
from pymongo.errors import DuplicateKeyError, OperationFailure
from bson.objectid import ObjectId
from bson.errors import InvalidId


def get_db():
    """
    Configuration method to return db instance
    """
    db = getattr(g, "_database", None)

    if db is None:

        db = g._database = PyMongo(current_app).db
       
    return db


# Use LocalProxy to read the global db instance with just `db`
db = LocalProxy(get_db)

def get_user(email: str):
    """
    Find the user record by email.
    - email
    """
    try:
        return list(db.users.find({},{"email": email}))
    except Exception as e:
        return e


def add_user(name: str, email: str, phone: str):
    """
    Inserts a new user into the users database from the registration page. Maintain variable total user.
    - "uuid"
    - "name"
    - "email"
    - "phone"
    - "timestamp"
    - "cherry"
    - "streak"
    - "health"
    - "xp"
    - "progress"
    """
    
    new_user = { 'uuid' : str(uuid.uuid4()), 'name' : name, 'email' : email,'phone' : phone, 'timestamp' : time.time(), 'cherry': 0, 'streak': 0, 'health': 5, 'xp': 100, 'progress': 0}
    return db.users.insert_one(new_user)


# def update_user(comment_id, user_email, text, date):
#     """
#     Updates the comment in the comment collection. Queries for the comment
#     based by both comment _id field as well as the email field to doubly ensure
#     the user has permission to edit this comment.
#     """
#     # TODO: Create/Update Comments
#     # Use the user_email and comment_id to select the proper comment, then
#     # update the "text" and "date" of the selected comment.
#     response = db.comments.update_one(
#         { "comment_id": comment_id },
#         { "$set": { "text ": text, "date" : date } }
#     )

#     return response
