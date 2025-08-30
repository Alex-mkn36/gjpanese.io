from flask import Flask, render_template, request, redirect, session
from gram import generate_sentence

app = Flask(__name__)
app.secret_key = "hi"

@app.route("/")
def Home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    level = request.form.get("level")
    grammar = request.form.get("grammar")
    sentence = generate_sentence(level, grammar)
    session['sentence'] = sentence
    return redirect("/result")

@app.route("/result")
def result():
    sentence = session.get('sentence')
    return render_template("result.html", sentence=sentence)

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
