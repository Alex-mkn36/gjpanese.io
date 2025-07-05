from flask import Flask, render_template, request, redirect, session

web = Flask(__name__)

@web.route("/")
def Home():
    return render_template("index.html")
