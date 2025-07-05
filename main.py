from flask import Flask, render_template, request, redirect, session
app = Flask(__name__)


@app.route("/")
def Home():
    return render_template("index.html")
