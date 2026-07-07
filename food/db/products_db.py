from database import *

def product_cat(name_category):
    conn = get_connection()
    cursor= conn.cursor()

    query = '''
            SELECT name, price
            FROM product p
            JOIN categori c ON p.category_id = c.category_id
            WHERE c.name_category = ?
            '''

    cursor.execute(query, (name_category,))
    result = cursor.fetchall()

    cursor.close()
    return result