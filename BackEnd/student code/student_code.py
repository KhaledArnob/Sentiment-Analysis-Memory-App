from flask import Flask, render_template, request, redirect, url_for, session
import csv
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')
app = Flask(__name__)
app.secret_key = "super_secret_key"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        with open("data/auth.csv", "a") as f:
            writer = csv.writer(f)
            writer.writerow([username, password])

        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        with open("data/auth.csv", "r") as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] == username and row[1] == password:
                    session["username"] = username
                    return redirect(url_for("profile"))

        return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")

def get_sentiment(score):
    if score >= 0.5:
        return 'Happy'
    elif score <= -0.5:
        return 'Sad'
    elif score > -0.5 and score < 0.5:
        return 'Neutral'
    else:
        return 'Angry'

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        text = request.form['text']
        sid = SentimentIntensityAnalyzer()
        sentiment = sid.polarity_scores(text)
        emotion = get_sentiment(sentiment['compound'])
        with open('data.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([text, emotion])
        return redirect(url_for('profile'))

    else:
        data = []
        with open('data.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                data.append(row)
        return render_template('profile.html', data=data)

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
