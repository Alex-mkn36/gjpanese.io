from flask import Flask, render_template, request, redirect, session

web = Flask(__name__)

@web.route("/")
def Home():
    return render_template("index.html")


web.run(debug=True, host="127.0.0.1", port=5000)
