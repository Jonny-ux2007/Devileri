import json
from flask import Flask, request, render_template, jsonify

from database import get_connection
from routes.orders import get_orders
from routes.users import get_users, create_user
from reg import *  
from menu import * 

app = Flask(__name__)
app.secret_key = 'супер_секретный_ключ_12345'
app.json.ensure_ascii = False 

@app.route("/")
def home():
    return "Добро пожаловать!"

@app.route("/autorization", methods=['GET', 'POST'])
def autorization():
    return autor()
    
@app.route("/menu")
def main_window():
   return menu()

if __name__ == "__main__":
    app.run(debug=True)