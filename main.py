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

class MyFormAdd(FlaskForm):
    movie_title = StringField('Movie Title', validators=[DataRequired()])



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

    movie_id_api = request.args.get("movie_id_api")
    if movie_id_api:

        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5YmY4NTI0NDliYWRhN2MwOTk1NGM2ZmZiODhmMTNjYSIsIm5iZiI6MTczMDAxNDA2MS45OTMzODcsInN1YiI6IjY3MWRlOTFmMWVhMzM5MjgyOTdkN2Y0YiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.riXtBNN7lgKfrJR5g2axHYC_uYvtGQr7r5NHraYF_1w"
        }
        response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id_api}", headers=headers)
        api_data_id = response.json()
        print(api_data_id['title'])

        new_movie_from_api = Movies(
            title=api_data_id['title'],
            year=api_data_id['release_date'],
            description=api_data_id['overview'],
            rating=7.3,
            ranking=10,
            review="My favourite character was the caller.",
            img_url= f"https://image.tmdb.org/t/p/w500{api_data_id['poster_path']}")

        db.session.add(new_movie_from_api)
        db.session.commit()
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

@app.route("/delete/<int:movie_id>")
def delete_movie(movie_id):
    movie_to_delete = db.get_or_404(Movies, movie_id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/add", methods=["GET", "POST"])

def add_movie():
    add = MyFormAdd()
    if add.validate_on_submit():
        movie_to_add = add.movie_title.data
        parameters = {
                    "query": movie_to_add

                }
        headers = {
                    "accept": "application/json",
                    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5YmY4NTI0NDliYWRhN2MwOTk1NGM2ZmZiODhmMTNjYSIsIm5iZiI6MTczMDAxNDA2MS45OTMzODcsInN1YiI6IjY3MWRlOTFmMWVhMzM5MjgyOTdkN2Y0YiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.riXtBNN7lgKfrJR5g2axHYC_uYvtGQr7r5NHraYF_1w"
                }
        response = requests.get("https://api.themoviedb.org/3/search/movie", headers=headers, params=parameters)
        api_data = response.json()["results"]
        # print(api_data)
        return render_template('select.html', datas = api_data)



    return render_template('add.html', form= add)




if __name__ == '__main__':
    app.run(debug=True)
