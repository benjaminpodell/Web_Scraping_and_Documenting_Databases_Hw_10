# Importing Dependencys
from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Creating Flask app Variable
app = Flask(__name__)

# Creating connection to Mongo DB
mongo = PyMongo(app)

# Creating a route that renders dat to the index.html
@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

# Establishing the scrape route seen in created html that pulls from mongo and updates with mars data
@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape()
    mars.update( {}, mars_data, upsert=True)
    
    # Redirects and returns the info to local host
    return redirect("http://localhost:5000/")

# Finalizing App
if __name__ == "__main__":
    app.run(debug=True)