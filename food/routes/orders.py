from database import *

def get_orders(order_id):
    conn = get_connection()

    cursor = conn.cursor()

    query = '''
        SELECT o.order_id,u.username 
        FROM orders o
        JOIN [user] u ON o.user_id = u.user_id
        WHERE o.order_id = ?
    '''
    
    cursor.execute(query, (order_id,))

    
    return cursor.fetchall()