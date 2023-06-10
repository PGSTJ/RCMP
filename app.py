import os
from flask import (Flask, redirect, render_template, request, send_file, session, url_for)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('K-Inventory.html')

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True)