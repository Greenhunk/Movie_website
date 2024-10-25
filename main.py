# from crypt import methods
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

# creating forms
class MyForm(FlaskForm):
    rating = StringField('Your Rating out of 10 e.g. 7.5', validators=[DataRequired()])
    review = StringField('Your Review', validators=[DataRequired()])

# CREATE DB
class Base(DeclarativeBase):
  pass
db = SQLAlchemy(model_class=Base)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies.db"
db.init_app(app)


# CREATE TABLE
class Movies(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True, nullable=True)
    year: Mapped[int] = mapped_column(nullable=True)
    description: Mapped[str] = mapped_column(nullable=True)
    rating: Mapped[float] = mapped_column(nullable=True)
    ranking: Mapped[int] = mapped_column(nullable=True)
    review: Mapped[str] = mapped_column(nullable=True)
    img_url: Mapped[str] = mapped_column(nullable=True)

with app.app_context():
    db.create_all()

with app.app_context():
    new_movie = Movies(
    title="Phone Booth",
    year=2002,
    description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
    rating=7.3,
    ranking=10,
    review="My favourite character was the caller.",
    img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg")
    # db.session.add(new_movie)
    # db.session.commit()
with app.app_context():
    second_movie = Movies (
    title = "Avatar The Way of Water",
    year = 2022,
    description = "Set more than a decade after the events of the first film, learn the story of the Sully family (Jake, Neytiri, and their kids), the trouble that follows them, the lengths they go to keep each other safe, the battles they fight to stay alive, and the tragedies they endure.",
    rating = 7.3,
    ranking = 9,
    review = "I liked the water.",
    img_url = "https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg")
    # db.session.add(second_movie)
    # db.session.commit()




@app.route("/")
def home():
    result = db.session.execute(db.select(Movies).order_by(Movies.title))
    all_movies = result.scalars()
    return render_template("index.html", movies = all_movies)

@app.route("/edit/<int:movie_id>", methods = ["GET", "POST"])
def rate_movie(movie_id):
    edit_form = MyForm()
    movie_to_update = db.get_or_404(Movies, movie_id)
    # result = db.session.execute(db.select(Movies).order_by(Movies.title))
    # movie_name = result.scalar_one()
    if edit_form.validate_on_submit():
        movie_to_update.rating = edit_form.rating.data
        movie_to_update.review = edit_form.review.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit.html', form=edit_form, movie=movie_to_update)


if __name__ == '__main__':
    app.run(debug=True)
