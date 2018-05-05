from database import Database
from user import User
from flask import Flask, render_template, session, redirect, request, url_for, g
import twitter_utils as tu
import requests


Database.initialize(database = "learning", user = "Anas", host = "localhost")

app = Flask(__name__)
app.secret_key = "1234"

@app.before_request
def load_user():
    if "screen_name" in session:
        g.user = User.load_from_db(session["screen_name"])

@app.route("/")
def homepage():
    return render_template("index.html")

@app.route("/login")
def twitter_login():
    if "screen_name" in session:
        return redirect(url_for("profile"))
    request_token = tu.request_token()
    session["request_token"] = request_token

    # Redirect to twitter
    return redirect(tu.request_token_url(request_token))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("homepage"))

@app.route("/auth/twitter")
def twitter_auth():
    auth_verifier = request.args.get("oauth_verifier")
    access_token = tu.access_token(session["request_token"], auth_verifier)

    user = User.load_from_db(access_token["screen_name"])
    if not user:
        user = User(access_token["screen_name"], access_token["oauth_token"],
                    access_token["oauth_token_secret"], None)
        user.save_to_db()
    session["screen_name"] = user.screen_name

    return redirect(url_for("profile"))

@app.route("/profile")
def profile():
    return render_template("profile.html", screen_name = g.user)

@app.route("/search")
def search():
    query = request.args.get("q")
    tweets = g.user.twitter_request("https://api.twitter.com/1.1/search/tweets.json?q={}".format(query))

    tweet_text = [{"text" :tweet["text"], "label" : ""} for tweet in tweets["statuses"]]

    for tweet in tweet_text:
        r = requests.post("http://text-processing.com/api/sentiment/", data = {"text": tweet["text"]})
        result = r.json( )
        tweet["label"] = result["label"]

    return render_template("search.html", content = tweet_text) # content used by jinja2

app.run(port=4995, debug=True)


