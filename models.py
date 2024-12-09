from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4

db = SQLAlchemy()

def get_uuid():
    return uuid4().hex

# AUTHENTICATION DB TABLE #

class User(db.Model):
    __tablename__ = "users" # Database Table Name
    id = db.Column(db.String(36), primary_key=True, unique=True, default=get_uuid)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)    
    
    
# EXPENSE DB TABLE - CREATE #

# class Expense(db.Model):
#     __tablename__ = "expense"
#     id = db.Column(db.Integer, primary_key=True)
#     category = db.Column(db.String(200), nullable=False)
#     date = db.Column(db.Date, nullable=False)
#     expense_name = db.Column(db.String(200), nullable=False)
#     currency = db.Column(db.String(3), nullable=False)
#     expense_amount = db.Column(db.Numeric(10,2), nullable=False)
#     user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)

#     # Establish relationship with the User model
#     user = db.relationship('User', backref=db.backref('expenses', lazy=True))
    
    
# class Income(db.Model):
#     __tablename__ = "income"
#     id = db.Column(db.Integer, primary_key=True)
#     category = db.Column(db.String(200), nullable=False)
#     date = db.Column(db.Date, nullable=False)
#     currency = db.Column(db.String(50), nullable=False)
#     income_amount = db.Column(db.Numeric(10,2), nullable=False)
#     user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)

#     # Establish relationship with the User model
#     user = db.relationship('User', backref=db.backref('income', lazy=True))
