from database import * # Импортируем подключение(всё) из файла database.py 

def get_orders(order_id):   # Функция для получения данных(по id заказа) 
    conn = get_connection() # Выполняем подключение к БД

    cursor = conn.cursor()  # Создаём  курсор, с помощью его происходит взаимодействие с БД 

    query = ''' # Сам запрос
        SELECT o.order_id,u.username    # Запрвшиваем айди заказа и имя пользователя который выполнил это заказ
        FROM orders o       # Данные берём их таблицы orders и даём ей псевданим o
        JOIN [user] u ON o.user_id = u.user_id      # Соеденяем с таблицей usres по общему пол
        WHERE o.order_id = ?    # берём занчения только по нужному id( в нашем случает 2)
    '''
    
    cursor.execute(query, (order_id,))   #execute = выполни этот запрос где 1 параметр это условие, а 2 это параметр по которому выполняется условие

    
    return cursor.fetchall()    # fetсhall забирает все найденные результаты