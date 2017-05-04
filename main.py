from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True      # displays runtime errors in the browser, too
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flicklist:MyNewPass@localhost/flicklist'

db = SQLAlchemy(app)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    watched = db.Column(db.Boolean)

    def __init__(self, name):
        self.name = name
        self.watched = False

    def __repr__(self):
        return '<Movie %r>' % self.name

# a list of movies that nobody should have to watch
terrible_movies = [
    "Gigli",
    "Star Wars Episode 1: Attack of the Clones",
    "Paul Blart: Mall Cop 2",
    "Nine Lives",
    "Starship Troopers"
]

def getCurrentWatchlist():
    # returns user's current watchlist -- a list of movies they want to see but haven't yet
    return Movie.query.all()

def getWatchedMovies():
    # For now, we are just pretending
    # returns the list of movies the user has already watched and crossed off
    return [ "The Matrix", "The Princess Bride", "Buffy the Vampire Slayer" ]


# Create a new route called RateMovie which handles a POST request on /rating-confirmation
@app.route("/rating-confirmation", methods=['POST'])
def RateMovie():
    movie = request.form['movie']
    rating = request.form['rating']
    #movie = "The Matrix"

    if movie not in getWatchedMovies():
        # the user tried to cross off a movie that isn't in their list,
        # so we redirect back to the front page and tell them what went wrong
        error = "'{0}' is not in your Watchlist, so you can't cross it off!".format(movie)

        # redirect to homepage, and include error as a query parameter in the URL
        return redirect("/?error=" + error)

    # if we didn't redirect by now, then all is well
    return render_template('rating-confirmation.html', movie=movie, rating=rating)


# Create a new route called MovieRatings which handles a GET on /ratings
@app.route("/ratings", methods=['GET'])
def MovieRatings():
    return render_template('ratings.html', movies = getWatchedMovies())


@app.route("/watched-it", methods=['POST'])
def watchMovie():
    watched_movie_id = request.form['watched-movie']

    watched_movie = Movie.query.get(watched_movie_id)
    if not watched_movie:
        return redirect("/?error=Attempt to watch a movie unknown to this database")

    # if we didn't redirect by now, then all is well
    return render_template('watched-it.html', watched_movie=watched_movie)

@app.route("/add", methods=['POST'])
def addMovie():
    # look inside the request to figure out what the user typed
    new_movie_name = request.form['new-movie']

    # if the user typed nothing at all, redirect and tell them the error
    if (not new_movie_name) or (new_movie_name.strip() == ""):
        error = "Please specify the movie you want to add."
        return redirect("/?error=" + error)

    # if the user wants to add a terrible movie, redirect and tell them the error
    if new_movie_name in terrible_movies:
        error = "Trust me, you don't want to add '{0}' to your Watchlist".format(new_movie_name)
        return redirect("/?error=" + error)

    movie = Movie(new_movie_name)
    db.session.add(movie)
    db.session.commit()
    return render_template('add-confirmation.html', movie=movie)

@app.route("/")
def index():
    encoded_error = request.args.get("error")
    return render_template('edit.html', watchlist=getCurrentWatchlist(), error=encoded_error and cgi.escape(encoded_error, quote=True))

if __name__ == "__main__":
    app.run()
