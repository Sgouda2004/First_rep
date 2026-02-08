import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("portfolio.db")   # creates portfolio.db file
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS messages
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT,
                  email TEXT,
                  message TEXT)''')
    conn.commit()
    conn.close()

# Home Page
@app.route("/")
def home():
    return render_template("index.html")

# About Page
@app.route("/about")
def about():
    return render_template("about.html")

# Contact Page
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]
        conn = sqlite3.connect("portfolio.db")
        c = conn.cursor()
        c.execute("INSERT INTO messages (name, email, message) VALUES (?, ?, ?)", 
                  (name, email, message))
        conn.commit()
        conn.close()
        return f"Thanks {name}! Your message has been received ✅"
    return render_template("contact.html")

@app.route("/messages")
def messages():
    conn = sqlite3.connect("portfolio.db")
    c = conn.cursor()
    c.execute("SELECT * FROM messages")
    all_messages = c.fetchall()
    conn.close()
    return render_template("messages.html", messages=all_messages)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
