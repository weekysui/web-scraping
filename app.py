from flask import Flask, render_template,redirect
from flask_pymongo import PyMongo
import scrape_mars

app=Flask(__name__)
mongo = PyMongo(app)
@app.route("/")
def index():
    try:
        mars_list = mongo.db.mars_list.find_one()
        return render_template("index.html",mars_dict=mars_list)
    except:
        return redirect("http://localhost:5000/scrape", code=302)

@app.route("/scrape")
def scrape():
    mars_list = mongo.db.mars_list
    mars_data = scrape_mars.scrape()
    mars_list.update(
        {},
        mars_data,
        upsert=True
    )
    return redirect("http://localhost:5000/", code=302)

if __name__=="__main__":
    app.run(debug=True)
