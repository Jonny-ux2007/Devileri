from database import get_connection

def create_user(username, password, role='user'):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = """
            INSERT INTO [user] (username, password, role) 
            VALUES (?, ?, ?)
        """
        cursor.execute(query, (username, password, role))
        

        conn.commit()
        

        cursor.execute("SELECT MAX(user_id) FROM [user]")
        new_user_id = cursor.fetchone()[0]
        print(f"Новый user_id: {new_user_id}")
        
        cursor.close()
        conn.close()
        
        return {
            "message": "Пользователь создан",
            "username": username,
            "user_id": new_user_id,
            "role": role
        }
    except Exception as e:
        import traceback
        print("\n=== КРИТИЧЕСКАЯ ОШИБКА В ТЕРМИНАЛЕ ===")
        traceback.print_exc()
        print("=====================================\n")
        return f"Ошибка на сервере: {e}", 500

def get_users():
    try: 
        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("SELECT username FROM [user]")

        users = cursor.fetchall()

        cursor.close()

        conn.close()
    
        return [user[0] for user in users]

    except Exception as e:
        import traceback
        print("\n=== КРИТИЧЕСКАЯ ОШИБКА В ТЕРМИНАЛЕ ===")
        traceback.print_exc()
        print("=====================================\n")
        return f"Ошибка на сервере: {e}", 500