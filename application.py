import os
import requests

from flask import Flask, session, render_template,request,redirect,url_for,session,jsonify
from flask_session import Session
# from sqlalchemy import create_engine
# from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import or_
from models import *


app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SESSION_PERMANENT"]=False
app.config["SESSION_TYPE"]="filesystem"
Session(app)
db.init_app(app)



# Set up database



def main():
    db.create_all()

if __name__ == "__main__":
    with app.app_context():
        main()


@app.route("/",methods=["POST","GET"])
def index():
    password=request.form.get("pass")
    user=request.form.get("user")
    val=password!=None and user!=None
    if val:
        if len(password) < 1 or len(user) < 1:
            return redirect(url_for("register",length=True))
        try:
           
            user=User(username=user,password=password)
            db.session.add(user)
            db.session.commit()
        except:
            return redirect(url_for("register",duplicate=True))
    if "username" in session:
        session["username"]=None
    
    return render_template("index.html",val=val,no=False)

@app.route("/login",methods=["POST"])
def login():
    username=request.form.get("username")
    password=request.form.get("password")
    

    user=User.query.filter_by(username=username,password=password).first()
    if user is not None:
        error=False
        session["username"]=username
        
        return render_template("login.html",username=username,error=error)
    else:
        error=True
        
        return render_template("index.html",val=False,no=True)

@app.route("/register")
def register():
    duplicate=bool(request.args.get("duplicate"))

    if duplicate is None:
        duplicate=False
    length=bool(request.args.get("length"))

    if length is None:
        length=False
    return render_template("register.html",duplicate=duplicate,length=length)

@app.route("/search",methods=["POST"])
def search():
    search=request.form.get("search")
    books=Book.query.filter(or_(Book.isbn.like("%"+search+"%"),Book.title.like("%"+search+"%"),Book.author.like("%"+search+"%"))).all()

    if books is None:
        error=True
    else:
        error=False
    return render_template("search.html",error=error,books=books)

@app.route("/search/<string:isbn>",methods=["POST","GET"])
def book(isbn):
    book=Book.query.get(isbn)
    if book is None:
        return render_template("search.html",error=True,books=None)
    else:

        rating=request.form.get("rating")
        comment=request.form.get("comment")
        username=session.get("username")
        if rating is not None:
           
            book.add_review(comment,rating,username)

        reviews=Review.query.filter_by(isbn=isbn).all()
        review=Review.query.filter_by(isbn=isbn,username=username).first()
        if review is None:
            sub=True
        else:
            sub=False
        
        avail=True
        
        key="OHgErp8ZfYnOa5EO4H4GQ"
        res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": key, "isbns": isbn})
        if res.status_code !=200:
            avail=False
        else:
            data=res.json()
            average=data['books'][0]['average_rating']
            count=data['books'][0]['work_ratings_count']
            print(f" Average rating is {average} Ratings count is {count}")




        return render_template("book.html",book=book,reviews=reviews,sub=sub,avail=avail,average=average,count=count)

@app.route("/api/<string:isbn>")
def info(isbn):
    book=Book.query.get(isbn)
    if book is None:
        return jsonify({"error":"Invalid ISBN"}),402
    else:
        title=book.title
        year=book.year
        author=book.author
        isbn=book.isbn

        key="OHgErp8ZfYnOa5EO4H4GQ"
        res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": key, "isbns": isbn})
        if res.status_code !=200:
            return jsonify({"title":title,"year":year,"author":author,"isbn":isbn})
        else:
            data=res.json()
            average=data['books'][0]['average_rating']
            count=data['books'][0]['work_ratings_count']
            return jsonify({"title":title,"year":year,"author":author,"isbn":isbn,"review_count":count,"average_score":average})








        
        

    







