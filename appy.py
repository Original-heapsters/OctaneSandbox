import os
from flask import Flask, render_template, json, jsonify, request, url_for, send_from_directory
from werkzeug.utils import secure_filename
from flasgger import Swagger


app = Flask(__name__)
swagger = Swagger(app)

@app.route('/')
def index():
    """Endpoint returning a blank index file
    """
    return "index"

@app.route('/hello')
def hello():
    """Endpoint returning a blank index file
    """
    return "Hello world!"

@app.route('/healthcheck')
def healthcheck():
    """Endpoint returning a blank index file
    """
    return "healthcheck"

@app.route('/user/id/temp')
def getUser():
    """Endpoint returning a blank index file
    """
    return "user/id/temp"

@app.route('/user/settings/id/temp')
def userSettings():
    """Endpoint returning a blank index file
    """
    return "/user/settings/id/temp"

@app.route('/search/lat/lon')
def search():
    """Endpoint returning a blank index file
    """
    return "/search/lat/lon"

@app.route('/place/lat/lon')
def place():
    """Endpoint returning a blank index file
    """
    return "/place/lat/lon"

@app.route('/collect/item/id')
def collect():
    """Endpoint returning a blank index file
    """
    return "/collect/item/id"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
