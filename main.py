from flask import Flask, request, redirect, render_template
import cgi

app = Flask(__name__)

app.config['DEBUG'] = True      # displays runtime errors in the browser, too






def get_current_watchlist():
    # returns user's current watchlist--hard coded for now
    return [ "Star Wars", "Minions", "Freaky Friday", "My Favorite Martian" ]

# a form for crossing off watched movies
# (first we build a dropdown from the current watchlist items)
crossoff_options = ""



    


# a list of movies that nobody should have to watch
terrible_movies = [
    "Gigli",
    "Star Wars Episode 1: Attack of the Clones",
    "Paul Blart: Mall Cop 2",
    "Nine Lives",
    "Starship Troopers"
]


@app.route("/crossoff", methods=['POST'])
def crossoff_movie():
    crossed_off_movie = request.form['crossed-off-movie']

    if crossed_off_movie not in get_current_watchlist():
        # the user tried to cross off a movie that isn't in their list,
        # so we redirect back to the front page and tell them what went wrong
        error = "'{0}' is not in your Watchlist, so you can't cross it off!".format(crossed_off_movie)

        # redirect to homepage, and include error as a query parameter in the URL
        return redirect("/?error=" + error)

    return render_template('crossoff.html',crossed_off_movie = crossed_off_movie)


@app.route("/add", methods=['POST'])
def add_movie():
    # look inside the request to figure out what the user typed
    new_movie = request.form['new-movie']

    # if the user typed nothing at all, redirect and tell them the error
    if (not new_movie) or (new_movie.strip() == ""):
        error = "Please specify the movie you want to add."
        return redirect("/?error=" + cgi.escape(error, quote=True))

    # if the user wants to add a terrible movie, redirect and tell them the error
    if new_movie in terrible_movies:
        error = "Trust me, you don't want to add '{0}' to your Watchlist".format(new_movie)
        return redirect("/?error=" + cgi.escape(error, quote=True))

    # 'escape' the user's input so that if they typed HTML, it doesn't mess up our site
    new_movie_escaped = cgi.escape(new_movie, quote=True)

    # build response content
    new_movie_element = "<strong>" + new_movie_escaped + "</strong>"
    sentence = new_movie_element + " has been added to your Watchlist!"
    content = "<p>" + sentence + "</p>"

    return content


@app.route("/")
def index():
    

    # if we have an error, make a <p> to display it
    error = request.args.get("error")
    if error:
        error_esc = cgi.escape(error, quote=True)
        error_element = error_esc
    else:
        error_element = ''

    

    return render_template('edit.html',movie_list = get_current_watchlist(),error = error_element)


app.run()
