import os
from flask import Flask, jsonify, render_template, request, redirect, session, url_for
from requests_oauthlib import OAuth2Session

app = Flask(__name__)

# Get this information by registering your app at https://developer.id.me
client_id              = '28bf5c72de76f94a5fb1d9454e347d4e'
client_secret          = '3e9f2e9716dba6ec74a2e42e90974828'
redirect_uri           = 'localhost:5000'
scope                  = 'login'
authorization_base_url = 'https://api.id.me/oauth/authorize'
token_url              = 'https://api.id.me/oauth/token'
attributes_url         = 'https://api.id.me/api/public/v3/attributes.json'

@app.route("/")

def demo():
    return render_template('index.html')

@app.route("/callback", methods=["GET"])
def callback():
    # Exchange your code for an access token
    idme  = OAuth2Session(client_id, redirect_uri=redirect_uri)
    print(f'idme: {idme}')
    token = idme.fetch_token(token_url, client_secret=client_secret, authorization_response=request.url)
    print(f'token: {token}')
    # At this point you can fetch a user's attributes but lets save
    # the token and show how this is done from a persisted token
    # in /profile.
    session['oauth_token'] = token

    return redirect(url_for('.profile'))

@app.route("/profile", methods=["GET"])
def profile():
    # Fetching the user's attributes using an OAuth 2 token.
    idme = OAuth2Session(client_id, token=session['oauth_token'])
    payload = idme.get(attributes_url).json()

    session['profile'] = 'true'
    return jsonify(payload)

if __name__ == "__main__":
    # This allows us to use a plain HTTP callback
    os.environ['DEBUG'] = "1"
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    app.secret_key = os.urandom(24)
    app.run(debug=True)
