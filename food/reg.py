from flask import request, jsonify, render_template,  redirect, session
from database import get_connection
from routes.users import get_users, create_user

def register():
    try:
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            
            if not username or not password:
                return render_template('auth.html', error="Имя и пароль обязательны!")
            
            users = get_users()
            if username in users:
                return render_template('auth.html', error="Пользователь с этим именем уже существует!")
            else:
                result = create_user(username, password, 'user')
                return render_template('auth.html', success=f"Пользователь {username} создан!")
        
        return render_template('auth.html')
    except Exception as e:
        return render_template('auth.html', error=f"Ошибка: {e}")

def login():
    try:
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            
            if not username or not password:
                return render_template('auth.html', error="Имя и пароль обязательны!")
            
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
                # СОХРАНЯЕМ ДАННЫЕ ПОЛЬЗОВАТЕЛЯ В СЕССИЮ
                session['username'] = username
                session['role'] = user[1]
                return redirect('/menu')
            else:
                return render_template('auth.html', error="Неверный логин или пароль!")
        
        return render_template('auth.html')
    except Exception as e:
        return render_template('auth.html', error=f"Ошибка: {e}")
def autor():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == "login":
            return login()
        elif action == "register":
            return register()
    
    return render_template('auth.html')