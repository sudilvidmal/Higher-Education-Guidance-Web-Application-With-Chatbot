from flask import Flask, request, redirect, session
import json
import random
import string
import requests
from urllib.parse import parse_qs, urlencode, urlparse
from dbconnect import insert_user_info
import atexit

app = Flask(__name__)
app.secret_key = "siri"

def read_creds(filename):
    with open(filename) as f:
        credentials = json.load(f)
    return credentials

creds = read_creds("client.json")
client_id, client_secret = creds["client_id"], creds["client_secret"]
redirect_uri = creds["redirect_uri"]

def create_CSRF_token():
    letters = string.ascii_lowercase
    token = "".join(random.choice(letters) for i in range(20))
    return token

def get_user_info(access_token):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "cache-control": "no-cache",
        "X-Restli-Protocol-Version": "2.0.0",
    }
    response = requests.get("https://api.linkedin.com/v2/userinfo", headers=headers)
    if response.status_code == 200:
        user_info = response.json()
        return user_info
    else:
        print("Failed to retrieve user information.")
        return None

def exchange_code_for_token(api_url, client_id, client_secret, redirect_uri, auth_code):
    token_endpoint = f"{api_url}/accessToken"
    payload = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": redirect_uri,
        "client_id": client_id,
        "client_secret": client_secret
    }
    response = requests.post(token_endpoint, data=payload)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        print("Failed to obtain access token.")
        return None


# Routes

@app.before_request
def before_request_func():
    pass

@app.route('/')
def index():
    # Redirect to the LinkedIn authorization page
    api_url = "https://www.linkedin.com/oauth/v2"
    csrf_token = create_CSRF_token()
    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "state": csrf_token,
        "scope": "profile,email,openid"
    }
    auth_url = f"{api_url}/authorization?{urlencode(params)}"
    return redirect(auth_url)

@app.route('/callback')
def callback():
    # Extract the authorization code from the request URL
    auth_code = request.args.get('code')

    if auth_code:
        # Continue with your authorization flow
        api_url = "https://www.linkedin.com/oauth/v2"
        access_token = exchange_code_for_token(api_url, client_id, client_secret, redirect_uri, auth_code)
        
        if access_token:
            user_info = get_user_info(access_token)
            if user_info:
                # Extract user information
                name = user_info.get("name", "")
                email = user_info.get("email", "")
                image = user_info.get("picture", "")

                # Print user information (for debugging purposes)
                print("User's information:")
                print("Name:", name)
                print("Email:", email)
                print("Profile picture:", image)

                # Insert user information into the database
                insert_user_info(name, email, image)

                # Redirect to https://google.com/ or any other desired URL
                return redirect("https://google.com/")
            else:
                print("Failed to retrieve user information.")
        else:
            print("Failed to obtain access token.")
    else:
        print("Authorization code not found in the URL.")
    return "Authorization failed."



@app.after_request
def after_request_func(response):
    return response

def clear_session():
    session.clear()

# Register the cleanup function
atexit.register(clear_session)

if __name__ == "__main__":
    app.run(debug=True)