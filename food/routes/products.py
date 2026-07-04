from database import get_connection

def get_products():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = '''
            SELECT product_id, name, price
            FROM product
        '''
        
        cursor.execute(query)
        products = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return products
    
    except Exception as e:
        import traceback
        print("\n=== КРИТИЧЕСКАЯ ОШИБКА В ТЕРМИНАЛЕ ===")
        traceback.print_exc()
        print("=====================================\n")
        return f"Ошибка на сервере: {e}", 500