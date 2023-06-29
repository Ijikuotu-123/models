from typing import List # can also import Dict
from db import db
# db.model is the base model and should be inherited by all available models
class ItemModel(db.Model): # db.model tells sqlalchemy that we are going to store and retrieve item in/from the database
    __tablename__ = "items"

    id = db.Column (db.Integer, primary_key = True)
    name = db.Column (db.String(80),nullable=False, unique = True)   # creating table
    price = db.Column (db.Float(precision=2),nullable=False)  # precision = 2 means 2 d.p
  
    store_id = db.Column (db.Integer, db.ForeignKey ("stores.id"), nullable=False) # joining the two tables(foreign key is needed)."stores" is the table's name
    store = db.relationship ("StoreModel")  # type of relationship. one item can be in one store. so store and not stores

    #order_id = db.column (db.integer, db.foreign_key ("orders.id"), nullable=False) it wont be needed because it means 
    # we must put in the order_id when creating items
    # order = db.relatioship("OrderModel")

    def __init__ (self, name:str , price:float, store_id: int): # with flask_marsh this wont be needed again
        self.name = name
        self.price = price
        self.store_id = store_id    #this is added because store_id is part of item data

    @classmethod()
    def find_item_by_name(cls, name:str) -> "ItemModel":
        return cls.query.filter_by(name=name).first()

    @classmethod()
    def find_item_by_id(cls, _id:int) ->"ItemModel":
        return cls.query.filter_by(id= _id).first()
    
    @classmethod()
    def find_all(cls) -> List["ItemModel"]:  # gives a list of items. the reason while list is still left above
        return cls.query.all()

    
    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

