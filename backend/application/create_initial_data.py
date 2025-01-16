from flask_security import SQLAlchemyUserDatastore, hash_password
from .extensions import db

def create_data(user_datastore : SQLAlchemyUserDatastore):

    user_datastore.find_or_create_role(name = "Admin", description = "This is the Administrator")
    user_datastore.find_or_create_role(name = "Sponsor", description = "This is a Sponsor")
    user_datastore.find_or_create_role(name = "Influencer", description = "This is an Influencer")

    if not user_datastore.find_user(username = "Admin"):
        user_datastore.create_user(username = "Admin", password = hash_password("12345"), roles = ['Admin'])
    
    # if not user_datastore.find_user(username = "Sponsor"):
    #     user_datastore.create_user(username = "Sponsor", password = hash_password("12345"), roles = ['Sponsor'])
    # if not user_datastore.find_user(username = "Influencer"):
    #     user_datastore.create_user(username = "Influencer", password = hash_password("12345"), roles = ['Influencer'])

    db.session.commit()