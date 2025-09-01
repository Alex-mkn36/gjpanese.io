from flask import Flask, render_template, request, redirect, session
from gram import generate_sentence, check
import random

app = Flask(__name__)
app.secret_key = "hi"


@app.route("/")
def home():
    session.clear()
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    session['level'] = request.form.get("level")
    session['grammar'] = request.form.get("grammar")
    return redirect("/loading/generate")

@app.route("/loading/<type>")
def loading(type):
    bg_map = {
        1: "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExbjBkNXMzajA1Ymd4d21waGRidzl3enp0MnhncjY1amtzNHcwZ3A2cSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/2SwbBd39ak7YY/giphy.gif",
        2: "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExcXdyMGdybXlyNnYyeTk2dWZodmNlbDNjNGYzY281NmxuYWd6bW9raCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/fhAwk4DnqNgw8/giphy.gif",
        3: "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExaXR2a3liNXBkczJqajIydWZibjZwOG5vcWxlNXRxMm56ZnkxN3dsayZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/jqwzq0LoZOfLqqJZ0b/giphy.gif",
        4: "https://media.tenor.com/6RT4QfZp9L8AAAAM/japanese-apologoize.gif",
        5: "https://media.tenor.com/mtdDpb3FcqwAAAAM/dear-diary-dear-diary-meme.gif",
        6: "https://media2.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3Y3NuaW0zdjdmcjB5bmZxZHB4ZzNoaXJxMHQxZmMxbzY3ZWFoMjE2ayZlcD12MV9naWZzX3NlYXJjaCZjdD1n/q2ePk5TyEq8da/200.webp",
        7: "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExaDg3enVhMjFzN3cwemdxN2ltNjl3a280Z2J6c2d5ZHptdzNxY2lwbiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/6OrCT1jVbonHG/giphy.gif",
        8: "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExaWQzOHN6bXMxNmw4bWtwY3cxYnh1MGs4aWd5ZWx3MW53c3VyMDNmYiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/1hXY6iNdTFpTW4je85/giphy.gif"
    }

    background = random.choice(list(bg_map.values()))
    return render_template("loading.html", background=background, type=type)

@app.route("/generate-sentence")
def generate_sentence_route():
    level = session.get("level")
    grammar = session.get("grammar")
    if level and grammar:
        sentence = generate_sentence(level, grammar)
        session['sentence'] = sentence
    return {"status": "done"}

@app.route("/check", methods=["POST"])
def submit_answer():
    session['answer'] = request.form.get("answer")
    return redirect("/loading/check")
    
@app.route("/check-sentence")
def check_sentence_route():
    answer = session.get("answer")
    grammar = session.get("grammar")
    if answer and grammar:
        marking = check(answer, grammar)
        session['marking'] = marking
    return {"status": "done"}


@app.route("/result")
def result():
    sentence = session.get('sentence')
    marking = session.get('marking')
    return render_template("result.html", sentence=sentence, marking=marking)

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
