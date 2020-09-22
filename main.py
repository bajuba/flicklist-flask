from flask import Flask
from random import shuffle

app = Flask(__name__)

app.config['DEBUG'] = True      # displays runtime errors in the browser, too

@app.route("/")
def index():
    # choose a movie by invoking our new function
    movie = get_random_movie()

    # build the response string
    content = "<h1>Movie of the Day</h1>"
    content += "<ul>"
    content += "<li>" + movie[0] + "</li>"
    content += "</ul>"

    # TODO: pick another random movie, and display it under
    # the heading "<h1>Tommorrow's Movie</h1>"
    content += "<h1>Tomorrow's Movie</h1>"
    content += "<ul>"
    content += "<li>" + movie[1] + "</li>"
    content += "</ul>"
    return content

def get_random_movie():
    newList = []
    # TODO: make a list with at least 5 movie titles
    movieList = ["The Big Lebowski","The Matrix","District 9","Equilibrium", "Minions"]
    # TODO: randomly choose one of the movies, and return it
    shuffle(movieList)
    newList.append(movieList[0])
    newList.append(movieList[1])
    return newList


app.run()
