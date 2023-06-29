from flask import request

from requests import respone   # this is needed for the email
from db import db
from models.confirmation import ConfirmationModel


# a model is what an object is:it properties and all the things it can perform(methods)
# sqlalchemy acts on models. its used for quering our models(methods) and  for creating tables
# always leave two lines before a class

class UserModel(db.Model): # adding (db.model) tells sqlalchemy that we want to store this model in the database
    __tablename__ ="users"

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), unique = True)
    password = db.Column(db.String(80))
    email = db.Columb(db.String(80), nullable=False, unique=True)
    confirmation = db.relationship("ConfirmationModel", lazy = "dynamic", cascade = "all,delete orphan")


""" when we link userschema and the table together using flask_marshmalolow... we lost some pieces of 
imformation. Before now,in the schema, username and password where required. To handle this change 
username and  password variables into:"""
username = db.Column(db.String(80),nullable = False, unique = True)
password = db.Column(db.String(80), nullable = False)



def __init__ (self,username: str, password: str):  # with flask_marsh this won't be needed again 
    self.username = username  # with flask_marsh this wont be needed again
    self.password = password   # with flask_marsh this wont be needed again

    @property
    def most_recent_confirmation(self) ->"ConfirmationModel":
        return self.confirmation.order_by (db.desc(ConfirmationModel.expired_at)).first()

    @classmethod
    def find_by_username(cls, username: str) ->"UserModel":
        return cls.query.filter_by(username = username).first()

    @classmethod
    def find_by_email(cls, email: str) ->"UserModel":
        return cls.query.filter_by(email = email).first()
   
    @classmethod
    def find_by_id (cls, _id: int) ->"UserModel":
        return cls.query.filter_by(id = _id).first()
    
    def send_confirmation_email(self)->Response: # this communicate with mailgun and return whatever it gives us
        # configure email content
        subject = "registration confirmation"
        link = request.url_root[:-1] + url_for("confirmation",confirmation_id = self.most_recent_confirmation.id) 
        # the id can aslo be user_id =self.id but we want it to be an id that can't be guessed
        # request.url_root[:-1]+ url_for = http://127.0.0.5000/confirmation/id
        # request.url_root[:-1] means  http://127.0.0.5000. normally,there's a /after 5000 but we aren't picking it
        # because the -1 means everything before  the last.request.url_root= http://127.0.0.5000/
        text = f" please click the link to confirm your registration:{link}"
        html = f"<html> please click the link to confirm your registration: <a href = {link}> link</a></html>"
        # send email mailgun
        return Mailgun.send_email([self.email], subject,text,html)

    def save_to_db (self) -> None:
        db.session.add(self)
        db.session.commit()
            
    def delete_from_db (self) -> None:
        db.session.delete(self)
        db.session.commit()
    


###########################################################################################
##########################  HARSING OF PASSWORD#################################################
from werkzeug.security import generate_password_hash,check_password_hash

# set the column password_hash = db.Column(db.String(80), nullable = False)

@property        #    we try to get the user password, this will be returned
def password(self):            
    raise AttributeError('password is not a readable attribute')

@password.setter
def password(self,password):
    self.password_hash = generate_password_harsh(password)

def verify_password(self,password):
    return check_password_hash(self.password_harsh, password)










   
   

