import pyodbc   # Библиотека для работы с БД

def get_connection():           # Функция котороя будет возращать подключение к БД
    conn = pyodbc.connect(      # Инициализация пременной conn объяетом подключения(несёт в себе подключение к БД)
        "DRIVER={ODBC Driver 17 for SQL Server};"   # Программа, через которую Python общается с SQL Server
        "SERVER=localhost;" # Адрес сервера(localhost потому что он у меня на компе) 
        "DATABASE=Food;"    # Имя базы данных к которой подключаемся
        "Trusted_Connection=yes;"   
    )
    return conn     # возвращение объекта подключения

import pyodbc 

