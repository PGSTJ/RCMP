import os
from flask import (Flask, redirect, render_template, request, send_file, session, url_for)
import Kitchen_Inventory.inventory as ki

app = Flask(__name__)

@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/Kitchen-Inventory', methods=['POST', 'GET'])
def inventory():
    inv_data = ki.extract_inventory()
    return render_template('K-Inventory.html', data=inv_data)

@app.route('/add_inventory', methods=['POST'])
def add_inventory():
    method = request.form['add_inventory']


    if method == 'Individual':
        # template section_add (should be same for restaurant)
        return render_template('section_add.html') # TODO: make template and add necessary variables
    elif method == 'CSV':
        pass # TODO: popup for CSV upload

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True)