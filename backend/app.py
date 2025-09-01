from flask import Flask, request, session, redirect, url_for
from markupsafe import escape
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("APP_SECRET_KEY")

@app.route("/")
def index():
    if "username" in session:
        return f"Logged in as {session['username']}"
    return "<h1>Subdomain Monitor</h1>"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["username"] = request.form["username"]
        return redirect(url_for("index"))
    return """
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    """

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))

@app.route("/api/subdomains")
def list_subdomains():
    domain = request.args.get("domain", "example.com")
    return f"List of {escape(domain)}"