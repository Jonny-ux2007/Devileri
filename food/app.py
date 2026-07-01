import json # Импортируем для вывода в консоль
from flask import Flask, jsonify # Добавляем jsonify
from database import get_connection
from routes.orders import get_orders

app = Flask(__name__)

# Настройка Flask, чтобы русский текст в JSON не превращался в коды \u043d
app.json.ensure_ascii = False 

def trycon():
    try:
        # 1. Получаем данные из базы (сейчас это tuple, например: (10, 5))
        db_data = get_orders(2) 
        
        if not db_data:
            return jsonify({"error": "Заказ не найден"}), 404
        
        # 2. Формируем понятный объект (словарь)
        # Внимание: индексы [0] и [1] зависят от того, что именно ваш get_orders выбирает в SELECT
        order_object = {
        "product_id": db_data[0][0],  # Первый элемент первого кортежа
        "user_id": db_data[0][1]     # Второй элемент первого кортежа
        }

        print(json.dumps(order_object, indent=4, ensure_ascii=False))

         # 4. Возвращаем JSON-ответ клиенту (в браузер)
        return jsonify(order_object)
    except Exception as e:
        import traceback
        print("\n=== КРИТИЧЕСКАЯ ОШИБКА В ТЕРМИНАЛЕ ===")
        traceback.print_exc() # Выведет точную строку и причину сбоя
        print("=====================================\n")
        return f"Ошибка на сервере: {e}", 500

@app.route("/orders")
def getProd():
    return trycon()


@app.route("/")
def home():
    return "Добро пожаловать!"

if __name__ == "__main__":
    app.run(debug=True)