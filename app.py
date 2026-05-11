from flask import Flask, render_template, request, redirect, session, flash
import sqlite3
from datetime import datetime

app = Flask(__name__)

app.secret_key = "supersecretkey"

ADMIN_PASSWORD = "mokshadmin"

# ---------------- DATABASE ----------------

def init_db():

    conn = sqlite3.connect("lines.db")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS lines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

init_db()

# ---------------- HOME ----------------

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        line = request.form.get("line")

        if not line or len(line.strip()) == 0:
            flash("Line cannot be empty.")
            return redirect("/")

        if len(line) > 180:
            flash("Maximum 180 characters allowed.")
            return redirect("/")

        conn = sqlite3.connect("lines.db")
        c = conn.cursor()

        c.execute(
            "INSERT INTO lines (text, created_at) VALUES (?, ?)",
            (
                line.strip(),
                datetime.now().strftime("%d %b %Y • %I:%M %p")
            )
        )

        conn.commit()
        conn.close()

        flash("Line saved.")

        return redirect("/")

    return render_template("index.html")

# ---------------- LOGIN ----------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        password = request.form.get("password")

        if password == ADMIN_PASSWORD:

            session["admin"] = True

            return redirect("/admin")

        flash("Wrong password.")

    return render_template("login.html")

# ---------------- ADMIN ----------------

@app.route("/admin")
def admin():

    if not session.get("admin"):
        return redirect("/login")

    conn = sqlite3.connect("lines.db")
    c = conn.cursor()

    c.execute("SELECT * FROM lines ORDER BY id DESC")

    lines = c.fetchall()

    conn.close()

    return render_template("admin.html", lines=lines)

# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")

if __name__ == "__main__":
    app.run()