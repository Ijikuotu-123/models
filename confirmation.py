from uuid import uuid4
from time import time
from db import db

CONFIRMATION_EXPIRATION_DELTA = 1800 # 30 minutes      # time it will last for 


class ConfirmationModel(db.model):
    __tablename__ = "confirmation"

id = db.Column(db.String(50), primary_key = True ) # id is not an integer because id will be a token for security reasons
expired_at = db.Column(db.integer,nullable = False ) #time
confirmed = db.Column(db.boolean,nullable = False )
user_id = db.Column(db.Integer,db.Foreignkey("users.id"),nullable = False)   # users is the table name. u in users must be in small letter
user = db.relationship("UserModel")

def __init__(self,user_id: int, **kwargs):
    super(). __init__ (**kwargs)
    self.user_id = user_id
    self.id = uuid4().hex
    self.expired_at = int(time()) + CONFIRMATION_EXPIRATION_DELTA
    self.confirmed = False
 
@ classmethod()
def find_by_id(cls, _id:str) ->"ConfirmationModel":
    return cls.query.filter_by(id= _id).first()

@property      # with this decorator i don't need to put () when i called this method
def expired(self) -> boolean:
    return time() > self.expired_at

def force_to_expire(self) -> None:
    if not self.expired:
        self.expired_at = int(time())
        self.save_to_db()

def save_to_db(self) -> None:
    db.session.add(self)
    db.session.committ()

def delete_from_db(self) ->None:
    db.session.delete(self)
    db.session.committ()




