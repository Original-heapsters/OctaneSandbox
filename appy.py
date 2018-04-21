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

@app.route('/user/settings/<userid>')
def userSettings(userid=None):
    """
        This is the endpoint to handle user settings configuration
    ---
    parameters:
      - in: path
        name: userid
        type: string
    responses:
      200:
        description: User settings updated
    """
    response = {}
    response["status"] = 200
    response["body"] = " User settings updated for UserID :" + userid
    response["userid"] = userid
    responseJSON = jsonify(response)
    return responseJSON

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

@app.route('/collect/<userid>/<itemid>')
def collect(userid=None, itemid=None):
    """
        This is the endpoint to handle adding an item to a users collection
    ---
    parameters:
      - in: path
        name: userid
        type: string
      - in: path
        name: itemid
        type: string
    responses:
      200:
        description: The task has been created
    """
    response = {}
    response["status"] = 200
    response["body"] = "UserID :" + userid + " ItemID : " + itemid
    response["userid"] = userid
    response["itemid"] = itemid
    responseJSON = jsonify(response)
    return responseJSON

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
