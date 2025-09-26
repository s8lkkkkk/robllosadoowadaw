from flask import Flask, render_template, request, jsonify, session
from datetime import datetime
import logging
import os

app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = os.environ.get("FLASK_SECRET", "change-me-in-production")

# Logging (no passwords)
logging.basicConfig(
    filename="login_attempts.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/attempt-login', methods=['POST'])
def attempt_login():
    """
    Receives { username } optionally from the front-end to log an attempt, then
    returns the official Roblox login URL. IMPORTANT: Passwords are NEVER accepted
    or forwarded in this endpoint.
    """
    data = request.get_json() or {}
    username = (data.get('username') or "").strip()

    if username:
        logging.info(f"Login attempt recorded for username='{username}'")
        session['last_attempt'] = {'username': username, 'timestamp': datetime.utcnow().isoformat()}
    else:
        logging.info("Login attempt recorded with empty username")
        session['last_attempt'] = {'username': None, 'timestamp': datetime.utcnow().isoformat()}

    return jsonify({
        "status": "ok",
        "redirect_url": "https://www.roblox.com/login",
        "message": "Redirecting to the official Roblox login page."
    })

@app.route('/last-attempt', methods=['GET'])
def last_attempt():
    return jsonify(session.get('last_attempt', {}))

if __name__ == '__main__':
    app.run(debug=True)
