from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, your app is running on Render!"
