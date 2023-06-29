import os
import stripe   # this must full be installed

from db import db
from typing import List

""" Many to Many Relationship""" 
# there is a problem with this method,in that an item can't appear more than once with an order id. ie.
# in an order , an we can't order for an item twice or more. this can be dealt with by adding the quatity 
# column but sqlalchemy does not like it as it's geared towards models and there is no way we can set the 
# quantity column
items_to_orders = db.Table(
    "items_to_orders",
    db.Column("item_id",db.Integer, db.ForeignKey ("items.id")),
    db.Column("order_id",db.Integer, db.ForeignKey ("orders.id"))
)

class OrderModel(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key = True)
    status =  db.Column(db.String(20), nullable = False)

    items = db.relationship("ItemModel", secondary = items_to_orders, lazy = dynamic)
    """ secondary tell sqlalchemy to look for the item_id inside the secondary table """


""" Association object"""

class ItemsInOrder(db.Model):
    __tablename__ = "items_in_order"

    id = db.Column(db.Integer, primary_key = True)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"))
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"))
    quantity = db.Column(db.Integer)
    
    """Add the relationship here"""
    item = db.relationship("ItemModel")
    order = db.relationship("OrderModel", back_populates = "items")

class OrderModel1(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key = True)
    status =  db.Column(db.String, nullable = False)

    items = db.relationship("ItemsInModel", back_populates ="order")


    #items = db.relationship("ItemModel", secondary=items_to_orders, lazy = dynamic)
    # we want our order to be linked to a number of times but our items won't know they are linked to that order
    # we can achieve this by a many to many relationship.this is solved by one more table 

    @property
    def description(self):
        # generate a simple string representing this order, in the format "5x chair, 2x tables"
        item_count = [f"{i.quantity} x {i.item.name}" for i in self.items]
        return "," .join(item_count)

    @property
    def amount(self):
        return int(sum([item_data.item.price * item_data.quantity for item_data in self.items]) *100)

    @classmethod()       # list of orders
    def find_all(cls) ->List["OrderModel"]:
        return cls.query.all()
    
    @classmethod()
    def find_by_id(cls, _id:int) -> "OrderModel":
        return cls.query.filter_by(id=_id).first()

    def charge_with_stripe(self, token:str)-> charge.stripe:
        stripe.api_key = os.getenv("STRIPE_API_KEY")
        return stripe.charge.create(
            amount=self.amount,
            currency= CURRENCY,
            description=self.description,
            source=token
        )

    def set_status(self, new_status:str) -> None:
        self.status = new_status
        self.save_to_db()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
    
    