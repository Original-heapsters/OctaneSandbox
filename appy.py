import os
from flask import Flask, render_template, json, jsonify, request, url_for, send_from_directory
from werkzeug.utils import secure_filename
from flasgger import Swagger
import oktaTest

cwd = os.path.dirname(os.path.realpath(__file__))
app = Flask(__name__,
            static_folder='dist',
            static_url_path='/assets',
            template_folder='{}/tools/templates'.format(cwd))
app.secret_key = 'SECRET KEY THAT YOU **MUST** CHANGE ON PRODUCTION SYSTEMS!'
allowed_issuers = []

public_key_cache = {}


swagger = Swagger(app)
okta = oktaTest.oktaTest()
okta.setup( pathToConfig = "Sample.okta.json")
@app.route('/')
def index():
    """Endpoint returning a blank index file
    ---
    responses:
     200:
       description: The index of app
   """


    return ("index")

@app.route('/hello/<hello>')
def hello(hello = None):
    """Endpoint returning a blank index file
    ---
     parameters:
     - name: hello
       in: path
       type: string
       required: false
       default: World!
       responses:
        200:
       description: A Hello World message

    """

    print(hello)
    return ("Hello"+ hello)

@app.route('/healthcheck')
def healthcheck():
    """Endpoint returning a blank index file
    ---
    responses:
      200:
       description: A healthcheck 

    """

    return ("healthcheck")

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

@app.route('/search/<lat>/<lon>')
def search(lat = None, lon = None):
    """Endpoint returning a blank index file
    ---
    parameters:
     - name: lat
       in: path
       type: string
       required: true
       default: None
     - name: lon
       in: path
       type: string
       required: true
       default: None
    responses:
     200:
       description: The latitude and longitude"

    """
    return ("search:"+ lat + "," + lon)

@app.route('/place/lat/lon')
def place():
    """Endpoint returning a blank index file
    """
    return "place/lat/lon"

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

#Review after Okta is setup    
@app.route("/authorization-code/login-redirect")
def auth_login_redirect():
    return "redirect"
    
@app.route("/authorization-code/login-custom")
def auth_login_custom():
    return ("Log in")

@app.route("/authorization-code/logout")
def auth_logout():
    session.clear()
    response = {}
    response["status"] = 200
    response["body"] = "Successfully loged out"
    responseJSON = jsonify(response)
    return responseJSON

 
#Will be in another clasee, db related   
@app.route("/authorization-code/profile")
def auth_profile():
    if 'user' not in session:
        return redirect(url_for('index'))
    response = {}
    response["status"] = 200
    response["body"] = "Fetched user"
    response["user"] = session['user']
    responseJSON = jsonify(response)
    return (responseJSON)

@app.route("/authorization-code/callback")
def auth_callback():
    (data, statusCode) = okta.auth_callback(request)
    if statusCode != 200:
        response = {}
        response["status"] = statusCode
        response["body"] = data
        responseJSON = jsonify(response)
        return responseJSON

    session["user"] = data
    response = {}
    response["status"] = statusCode
    response["body"] = "Callback success"
    responseJSON = jsonify(response)
    return responseJSON


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
