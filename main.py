from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books-collection.db'

# Create the extension with the app
db = SQLAlchemy(app)

# Create a table
class Book(db.Model):
    __tablename__ = 'My Favorite Books'
    id = db.Column(db.Integer, primary_key=True)
    title: Mapped[str] = db.Column(db.String(250), nullable=False)
    author: Mapped[str] = db.Column(db.String(250), nullable=False)
    rating: Mapped[float] = db.Column(db.Float, nullable=False)

    # Allow the field to be identified by the title
    def __repr__(self):
        return f'<Book {self.title}>'

# Create the table schema. It requires application context.
with app.app_context():
    db.create_all()


@app.route('/')
def home():
    # Query all books from the database instead of using in-memory list
    with app.app_context():
        all_books = db.session.execute(db.select(Book)).scalars().all()
    return render_template("index.html", books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        try:
            with app.app_context():
                book = Book(
                    title=request.form["title"], 
                    author=request.form["author"], 
                    rating=float(request.form["rating"])
                )
                db.session.add(book)
                db.session.commit()
            print("Book added successfully!")
        except Exception as e:
            print(f"Error: {e}")
            return "Something went wrong!"

        return redirect(url_for('home'))

    return render_template("add.html")


if __name__ == "__main__":
    app.run(debug=True)