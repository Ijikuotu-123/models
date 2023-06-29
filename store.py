from typing import List
from db import db

# if it were a dictionary we would need dict from typing

class StoreModel(db.Model): # db.model tells sqlalchemy that we are going to store and retrieve 'stores' from the database
    __tablename__ = "stores"

    id = db.Column (db.Integer, primary_key = True)
    name = db.Column (db.String(80), nullable=False, unique = True)   # creating table
    items = db.relationship('ItemModel', lazy = dynamic)  # relationship type. one store can have many items.
    # don't add nullable to items because it's a relation

    def __init__ (self, name:str ):        # with flask_marsh this wont be needed again
        self.name = name
        

    @classmethod()
    def find_store_by_name(cls, name:str) -> "StoreModel":
        return cls.query.filter_by(name=name).first()

    @classmethod()
    def find_all(cls) -> List["StoreModel"]:
        return cls.query.all()
    
    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

