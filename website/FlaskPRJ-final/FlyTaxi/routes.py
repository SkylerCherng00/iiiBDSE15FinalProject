from flask import render_template, url_for
from FlyTaxi import app
from FlyTaxi import models

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', strgeo=models.geoInfo(), clustersInfo=models.clusterInfo())


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/analysis")
def analysis():
    return render_template('analysis.html')
