import json
from flask import Flask, request, render_template, jsonify, redirect, session
from database import get_connection
from routes.products import *

def menu():
    try:   
        
        username = session.get('username')
        role = session.get('role')
        
        if not username:
            return redirect('/autorization')
        
        # ПОЛУЧАЕМ ПРОДУКТЫ ИЗ БД
        products = get_products()
        
        # ПРИВЕТСТВИЕ
        if role == 'admin':
            welcome = f" Добро пожаловать,{username}({role}) "
        elif role == 'manager':
            welcome = f"Добро пожаловать,{username}({role})"
        elif role == 'courier':
            welcome = f"Добро пожаловать,{username}({role})"
        else:
            welcome = f"Добро пожаловать,{username}({role})"
        
        return render_template('menu.html', welcome=welcome, products=products)

    except Exception as e:
            import traceback
            print("\n=== КРИТИЧЕСКАЯ ОШИБКА В ТЕРМИНАЛЕ ===")
            traceback.print_exc()
            print("=====================================\n")
            return f"Ошибка на сервере: {e}", 500    