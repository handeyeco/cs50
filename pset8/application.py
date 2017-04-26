import os
import re
from flask import Flask, jsonify, render_template, request, url_for
from flask_jsglue import JSGlue

from cs50 import SQL
from helpers import lookup
from location import Location

# configure application
app = Flask(__name__)
JSGlue(app)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///mashup.db")

@app.route("/")
def index():
    """Render map."""
    if not os.environ.get("API_KEY"):
        raise RuntimeError("API_KEY not set")
    return render_template("index.html", key=os.environ.get("API_KEY"))

@app.route("/articles")
def articles():
    """Look up articles for geo."""
    geo = request.args.get('geo')
    articles = lookup(geo)
    # TODO
    return jsonify(articles)

@app.route("/search")
def search():
    """Search for places that match query."""
    query = request.args.get('q')
    query = re.sub("\+", " ", query)
    l = Location(query)
    if l.city:
        city = l.city + "%"
    if l.state:
        state = l.state + "%"
    if l.zipcode:
        zipcode = l.zipcode + "%"
    result = []

    if l.city and l.state and l.zipcode:
        result = db.execute("SELECT * FROM places WHERE place_name LIKE :place_name AND admin_name1 LIKE :admin_name1 AND postal_code LIKE :postal_code", place_name=city, admin_name1=state, postal_code=zipcode)
    elif l.city and l.zipcode:
        result = db.execute("SELECT * FROM places WHERE place_name LIKE :place_name AND postal_code LIKE :postal_code", place_name=city, postal_code=zipcode)
    elif l.city and l.state:
        result = db.execute("SELECT * FROM places WHERE place_name LIKE :place_name AND admin_name1 LIKE :admin_name1", place_name=city, admin_name1=state)
    elif l.state and l.zipcode:
        result = db.execute("SELECT * FROM places WHERE admin_name1 LIKE :admin_name1 AND postal_code LIKE :postal_code", admin_name1=state, postal_code=zipcode)
    elif l.city:
        result = db.execute("SELECT * FROM places WHERE place_name LIKE :place_name", place_name=city)
    elif l.state:
        result = db.execute("SELECT * FROM places WHERE admin_name1 LIKE :admin_name1", admin_name1=state)
    elif l.zipcode:
        result = db.execute("SELECT * FROM places WHERE postal_code LIKE :postal_code", postal_code=zipcode)

    return jsonify(result)

@app.route("/update")
def update():
    """Find up to 10 places within view."""

    # ensure parameters are present
    if not request.args.get("sw"):
        raise RuntimeError("missing sw")
    if not request.args.get("ne"):
        raise RuntimeError("missing ne")

    # ensure parameters are in lat,lng format
    if not re.search("^-?\d+(?:\.\d+)?,-?\d+(?:\.\d+)?$", request.args.get("sw")):
        raise RuntimeError("invalid sw")
    if not re.search("^-?\d+(?:\.\d+)?,-?\d+(?:\.\d+)?$", request.args.get("ne")):
        raise RuntimeError("invalid ne")

    # explode southwest corner into two variables
    (sw_lat, sw_lng) = [float(s) for s in request.args.get("sw").split(",")]

    # explode northeast corner into two variables
    (ne_lat, ne_lng) = [float(s) for s in request.args.get("ne").split(",")]

    # find 10 cities within view, pseudorandomly chosen if more within view
    if (sw_lng <= ne_lng):

        # doesn't cross the antimeridian
        rows = db.execute("""SELECT * FROM places
            WHERE :sw_lat <= latitude AND latitude <= :ne_lat AND (:sw_lng <= longitude AND longitude <= :ne_lng)
            GROUP BY country_code, place_name, admin_code1
            ORDER BY RANDOM()
            LIMIT 10""",
            sw_lat=sw_lat, ne_lat=ne_lat, sw_lng=sw_lng, ne_lng=ne_lng)

    else:

        # crosses the antimeridian
        rows = db.execute("""SELECT * FROM places
            WHERE :sw_lat <= latitude AND latitude <= :ne_lat AND (:sw_lng <= longitude OR longitude <= :ne_lng)
            GROUP BY country_code, place_name, admin_code1
            ORDER BY RANDOM()
            LIMIT 10""",
            sw_lat=sw_lat, ne_lat=ne_lat, sw_lng=sw_lng, ne_lng=ne_lng)

    # output places as JSON
    return jsonify(rows)
