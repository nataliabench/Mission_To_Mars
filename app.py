# Import Tools
# Use Flask to render a template
from flask import Flask, render_template, redirect

# Use PyMongo to interact with our Mongo database
from flask_pymongo import PyMongo

# Convert from Jupyter notebook to Python to use scraping code
import scraping

# Setup Flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
# app.config["MONGO_URI"] tells Python that app will connect to Mongo using a URI, a uniform resource identifier, similar to a URL
# "mongodb://localhost:27017/mars_app" is the URI used to connect the app to Mongo. 
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Define the route for the HTML page
# @app.route("/"), tells Flask what to display when looking at the home page
# mars = mongo.db.mars.find_one() uses PyMongo to find the "mars" collection in the database
# return render_template("index.html" tells Flask to return an HTML template using an index.html file
# mars=mars) tells Python to use the "mars" collection in MongoDB
@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)

# Set up scraping route
# @app.route(“/scrape”) defines the route that Flask will be using
# This route, “/scrape”, will run the function that is created below
# Next lines allow access to the database, scrape new data using scraping.py script, update the database, and return a message when successful
# Define it with def scrape()
# Assign a new variable that points to our Mongo database: mars = mongo.db.mars
# Create a new variable to hold the newly scraped data: mars_data = scraping.scrape_all()
# Use .update(), add add an empty JSON object with {} given data is being inserted 
# upsert=True indicates to Mongo to create a new document if one doesn't already exist, and new data will always be saved (even if a document hasn't already been created for it)
# Add a redirect after successfully scraping the data to navigate the page back to / where the updated content can be seen
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update({}, mars_data, upsert=True)
   return redirect('/', code=302)

# Run Flask
if __name__ == "__main__":
   app.run()