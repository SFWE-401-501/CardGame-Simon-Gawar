from flask import Flask, request # type: ignore
from flask_httpauth import HTTPBasicAuth # type: ignore

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {"admin": "password"}

@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username

@app.route('/secure-data')
@auth.login_required
def secure_data():
    return "Sensitive Data Accessed Securely"
