from flask import request, jsonify, render_template
from database import get_connection
from routes.users import get_users, create_user

def register():
    try:
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            role = request.form.get('role', 'user')
            
            if not username or not password:
                return "Имя и пароль обязательны!"
            
            users = get_users()
            if username in users:
                return "Пользователь с этим именем уже существует!"
            else:
                result = create_user(username, password, role)
                return jsonify(result)
        
        return '''
        <form method="POST">
            <input type="text" name="username" placeholder="Имя" required><br>
            <input type="password" name="password" placeholder="Пароль" required><br>
            <button type="submit">Создать пользователя</button>
        </form>
        '''
    except Exception as e:
        import traceback
        print("\n=== КРИТИЧЕСКАЯ ОШИБКА В ТЕРМИНАЛЕ ===")
        traceback.print_exc()
        print("=====================================\n")
        return f"Ошибка на сервере: {e}", 500

def login():
    try:
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            
            if not username or not password:
                return "Имя и пароль обязательны!"
            
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT user_id, role FROM [user] WHERE username = ? AND password = ?",
                (username, password)
            )
            user = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if user:
                return f"Добро пожаловать, {username}! (Роль: {user[1]})"
            else:
                return "Неверный логин или пароль!"
        
        return '''
        <form method="POST">
            <input type="text" name="username" placeholder="Логин" required><br>
            <input type="password" name="password" placeholder="Пароль" required><br>
            <input type="text" name="role" placeholder="Роль (user/admin)" value="user"><br>
            <button type="submit">Войти</button>
        </form>
        '''
    except Exception as e:
        import traceback
        print("\n=== КРИТИЧЕСКАЯ ОШИБКА В ТЕРМИНАЛЕ ===")
        traceback.print_exc()
        print("=====================================\n")
        return f"Ошибка на сервере: {e}", 500

def autor():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == "login":
            return login()
        elif action == "register":
            return register()
    
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Вход / Регистрация</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Segoe UI', Tahoma, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
            }
            .container {
                background: white;
                border-radius: 20px;
                padding: 40px;
                width: 400px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            }
            h2 {
                text-align: center;
                color: #333;
                margin-bottom: 25px;
                font-size: 28px;
            }
            .tabs {
                display: flex;
                margin-bottom: 25px;
                border-bottom: 2px solid #eee;
            }
            .tab {
                flex: 1;
                padding: 10px;
                text-align: center;
                cursor: pointer;
                font-weight: 600;
                color: #888;
                border-bottom: 3px solid transparent;
            }
            .tab.active {
                color: #667eea;
                border-bottom-color: #667eea;
            }
            .form-group {
                margin-bottom: 15px;
            }
            .form-group label {
                display: block;
                margin-bottom: 5px;
                font-weight: 500;
                color: #555;
                font-size: 14px;
            }
            .form-group input {
                width: 100%;
                padding: 12px;
                border: 2px solid #e0e0e0;
                border-radius: 10px;
                font-size: 14px;
                outline: none;
                transition: 0.3s;
            }
            .form-group input:focus {
                border-color: #667eea;
                box-shadow: 0 0 0 3px rgba(102,126,234,0.2);
            }
            .btn {
                width: 100%;
                padding: 14px;
                border: none;
                border-radius: 10px;
                font-size: 16px;
                font-weight: 600;
                color: white;
                cursor: pointer;
                transition: 0.3s;
                margin-top: 5px;
            }
            .btn-login {
                background: linear-gradient(135deg, #667eea, #764ba2);
            }
            .btn-login:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 20px rgba(102,126,234,0.4);
            }
            .btn-register {
                background: linear-gradient(135deg, #11998e, #38ef7d);
            }
            .btn-register:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 20px rgba(56,239,125,0.4);
            }
            .hidden { display: none; }
            .divider {
                text-align: center;
                color: #ccc;
                margin: 20px 0;
                font-size: 12px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2> Доставка еды</h2>
            
            <div class="tabs">
                <div class="tab active" onclick="switchTab('login')" id="tab-login">Вход</div>
                <div class="tab" onclick="switchTab('register')" id="tab-register">Регистрация</div>
            </div>
            
            <!-- ВХОД -->
            <div id="form-login">
                <form method="POST">
                    <div class="form-group">
                        <label>Логин</label>
                        <input type="text" name="username" placeholder="Введите логин" required>
                    </div>
                    <div class="form-group">
                        <label>Пароль</label>
                        <input type="password" name="password" placeholder="Введите пароль" required>
                    </div>
                    <button type="submit" name="action" value="login" class="btn btn-login">Войти</button>
                </form>
            </div>
            
            <!-- РЕГИСТРАЦИЯ -->
            <div id="form-register" class="hidden">
                <form method="POST">
                    <div class="form-group">
                        <label>Имя пользователя</label>
                        <input type="text" name="username" placeholder="Придумайте логин" required>
                    </div>
                    <div class="form-group">
                        <label>Пароль</label>
                        <input type="password" name="password" placeholder="Придумайте пароль" required>
                    </div>
                    <button type="submit" name="action" value="register" class="btn btn-register">Зарегистрироваться</button>
                </form>
            </div>
            
            <div class="divider">🍕</div>
        </div>
        
        <script>
            function switchTab(type) {
                document.getElementById('form-login').className = type === 'login' ? '' : 'hidden';
                document.getElementById('form-register').className = type === 'register' ? '' : 'hidden';
                document.getElementById('tab-login').className = 'tab' + (type === 'login' ? ' active' : '');
                document.getElementById('tab-register').className = 'tab' + (type === 'register' ? ' active' : '');
            }
        </script>
    </body>
    </html>
    '''