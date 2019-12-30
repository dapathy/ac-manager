from flask import Flask
import os
import json

from flask import Flask, redirect, request, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from oauthlib.oauth2 import WebApplicationClient
import requests

from user import User

# Configuration
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "528797610245-ko6hnrl4d08qcfnt8k2tsqdju4ria97g.apps.googleusercontent.com")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

app = Flask(__name__)
port = int(os.environ.get("PORT", 5000))

login_manager = LoginManager()
login_manager.init_app(app)
client = WebApplicationClient(GOOGLE_CLIENT_ID)

@app.route("/")
def index():
    if current_user.is_authenticated:
        return (
            "<p>Hello, {}! You're logged in! Email: {}</p>"
            "<div><p>Google Profile Picture:</p>"
            '<img src="{}" alt="Google profile pic"></img></div>'
            '<a class="button" href="/logout">Logout</a>'.format(
                current_user.name, current_user.email, current_user.profile_pic
            )
        )
    else:
        return '<a class="button" href="/login">Google Login</a>'

@app.route("/login")
def login():
    authorization_endpoint = get_openid_configuration()["authorization_endpoint"]

    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

@app.route("/login/callback")
def callback():
    code = request.args.get("code")
    openid_configuration = get_openid_configuration()
    token_endpoint = openid_configuration["token_endpoint"]

    # get access token using code
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )
    client.parse_request_body_response(json.dumps(token_response.json()))
    
    # Get user info
    userinfo_endpoint = openid_configuration["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    userinfo_json = userinfo_response.json()
    unique_id = userinfo_json["sub"]
    users_email = userinfo_json["email"]
    picture = userinfo_json["picture"]
    users_name = userinfo_json["given_name"]

    user = User(
        id_=unique_id, name=users_name, email=users_email, profile_pic=picture
    )
    login_user(user)
    return redirect(url_for("index"))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

def get_openid_configuration():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=port)