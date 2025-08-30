from flask import Flask, render_template, request, redirect, session
import gram

app = Flask(__name__)
app.secret_key = "GJPN"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/choose", methods=["GET", "POST"])
def chose():
    japanese_text = None
    print("hi")
    if request.method == "POST":
        grammar = request.form.get("grammar")
        level = request.form.get("level")
        print("in post")
        try:
            japanese_text = gram.load_example(level, grammar)
        except Exception as e:
            print("Error in gram.load_example:", e)
            japanese_text = "Error generating example."
        print("after load")
        print(japanese_text+"hello")
        session['japanese_text'] = japanese_text
        return redirect("/example")
    return render_template("choose.html", sentence=japanese_text)

@app.route("/example")
def example():
    sentencedata = session.get("japanese_text", None)
    return render_template("example.html", sentence=sentencedata)


app.run(debug=True, port=5000, use_reloader=False)
