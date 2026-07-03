import json
from flask import Flask, request, render_template, jsonify

from database import get_connection
from routes.orders import get_orders
from routes.users import get_users, create_user
from reg import *  # ← reg.py должен быть в той же папке!

app = Flask(__name__)
app.json.ensure_ascii = False 

def trycon():
    try:
        db_data = get_orders(2) 
        
        if not db_data:
            return jsonify({"error": "Заказ не найден"}), 404
        
        order_object = {
            "product_id": db_data[0][0],
            "user_id": db_data[0][1]
        }

        print(json.dumps(order_object, indent=4, ensure_ascii=False))
        return jsonify(order_object)
        
    except Exception as e:
        import traceback
        print("\n=== КРИТИЧЕСКАЯ ОШИБКА В ТЕРМИНАЛЕ ===")
        traceback.print_exc()
        print("=====================================\n")
        return f"Ошибка на сервере: {e}", 500

@app.route("/orders")
def getOrd():
    return trycon()

@app.route("/")
def home():
    return "Добро пожаловать!"

@app.route("/autorization", methods=['GET', 'POST'])
def autorization():
    return autor()
    

if __name__ == "__main__":
    app.run(debug=True)