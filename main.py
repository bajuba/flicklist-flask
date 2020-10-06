from flask import Flask, request, redirect

app = Flask(__name__)

app.config['DEBUG'] = True      # displays runtime errors in the browser, too

#creating the function to return the movie_list
movie_list = ["movie1","movie2","movie3", "IT"]

def fetch_movie_list():
    return movie_list

page_header = """
<!DOCTYPE html>
<html>
    <head>
        <title>FlickList</title>
    </head>
    <body>
        <h1>FlickList</h1>
"""

page_footer = """
    </body>
</html>
"""

# a form for adding new movies
add_form = """
    <form action="/add" method="post">
        <label>
            I want to add
            <input type="text" name="new-movie"/>
            to my watchlist.
        </label>
        <input type="submit" value="Add It"/>
    </form>
"""

# a form for crossing off watched movies
crossoff_form1 = """
    <form action="/crossoff" method="post">
        <label>
            I want to cross off
            <select name="crossed-off-movie"/>
"""


crossoff_options = ""
for movie in fetch_movie_list():
    crossoff_options += "<option>" + movie + "</option>"


crossoff_form2 =""" 
"<option>Fake Movie"</option>"
            </select>
            from my watchlist.
        </label>
        <input type="submit" value="Cross It Off"/>
    </form>
"""


@app.route("/crossoff", methods=['POST'])
def crossoff_movie():
    crossed_off_movie = request.form['crossed-off-movie']

    #check if the movie is in the list

    if crossed_off_movie in fetch_movie_list():
        crossed_off_movie_element = "<strike>" + crossed_off_movie + "</strike>"
        confirmation = crossed_off_movie_element + " has been crossed off your Watchlist."
        content = page_header + "<p>" + confirmation + "</p>" + page_footer
        return content
    return redirect('/?error=That movie does not exist in your movie list')


    


@app.route("/add", methods=['POST'])
def add_movie():
    new_movie = request.form['new-movie']

    # build response content
    new_movie_element = "<strong>" + new_movie + "</strong>"
    sentence = new_movie_element + " has been added to your Watchlist!"
    content = page_header + "<p>" + sentence + "</p>" + page_footer

    return content


@app.route("/")
def index():
    new_error = ""
    if request.args.get("error"):
        new_error = request.args.get("error")
    edit_header = "<h2>Edit My Watchlist</h2>"

    # build the response string
    content = new_error+page_header + edit_header + add_form + crossoff_form1 +crossoff_options+crossoff_form2  + page_footer

    return content


app.run()

