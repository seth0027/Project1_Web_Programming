from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

class User(db.Model):
    __tablename__="users"
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String,nullable=False)
    password=db.Column(db.String,nullable=False)
  
class Book(db.Model):
    __tablename__="books"
    
    
    isbn=db.Column(db.String,primary_key=True)
    title=db.Column(db.String,nullable=False)
    author=db.Column(db.String,nullable=False)
    year=db.Column(db.Integer,nullable=False)

    def add_review(self,comment,rating,username,user_id):
        isbn=self.isbn
        review=Review(comment=comment,rating=rating,isbn=isbn,username=username,user_id=user_id)
        db.session.add(review)
        db.session.commit()

class Review(db.Model):
    __tablename__="reviews"
    id=db.Column(db.Integer,primary_key=True)
    comment=db.Column(db.String,nullable=True)
    rating=db.Column(db.String,nullable=False)
    isbn=db.Column(db.String,nullable=False)
    user_id=db.Column(db.Integer,nullable=False)
    username=db.Column(db.String,nullable=False)


    

