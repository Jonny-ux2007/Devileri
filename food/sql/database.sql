CREATE DATABASE Food;
GO

USE Food;
GO

IF OBJECT_ID('orders', 'U') IS NOT NULL DROP TABLE orders;
IF OBJECT_ID('product', 'U') IS NOT NULL DROP TABLE product;
IF OBJECT_ID('categori', 'U') IS NOT NULL DROP TABLE categori;
IF OBJECT_ID('courier', 'U') IS NOT NULL DROP TABLE courier;
IF OBJECT_ID('user', 'U') IS NOT NULL DROP TABLE [user];

-- 1. ПОЛЬЗОВАТЕЛИ

CREATE TABLE [user] (
    user_id INT IDENTITY(1,1) PRIMARY KEY,
    username NVARCHAR(50) NOT NULL UNIQUE,
    password NVARCHAR(255) NOT NULL,
    role NVARCHAR(20) NOT NULL CHECK(role IN ('user', 'admin', 'manager', 'courier')) DEFAULT 'user',
    created_at DATETIME DEFAULT GETDATE()
);


-- 2. КУРЬЕРЫ

CREATE TABLE courier (
    courier_id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(100) NOT NULL,
    is_active NVARCHAR(10) NOT NULL DEFAULT 'True',
    old INT CHECK(old BETWEEN 16 AND 50),
    created_at DATETIME DEFAULT GETDATE()
);


-- 3. КАТЕГОРИИ

CREATE TABLE categori (
    category_id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(50) NOT NULL UNIQUE
);


-- 4. ПРОДУКТЫ

CREATE TABLE product (
    product_id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(100) NOT NULL UNIQUE,
    price DECIMAL(10,2) NOT NULL CHECK(price > 0),
    category_id INT NOT NULL,
    CONSTRAINT FK_product_categori FOREIGN KEY (category_id) REFERENCES categori(category_id)
);


-- 5. ЗАКАЗЫ

CREATE TABLE orders (
    order_id INT IDENTITY(1,1) PRIMARY KEY,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    courier_id INT NULL,
    quantity INT DEFAULT 1 CHECK(quantity > 0),
    status NVARCHAR(20) NOT NULL CHECK(status IN ('new', 'waiting', 'done', 'rejected')) DEFAULT 'new',
    created_at DATETIME DEFAULT GETDATE(),
    CONSTRAINT FK_orders_user FOREIGN KEY (user_id) REFERENCES [user](user_id),
    CONSTRAINT FK_orders_product FOREIGN KEY (product_id) REFERENCES product(product_id),
    CONSTRAINT FK_orders_courier FOREIGN KEY (courier_id) REFERENCES courier(courier_id)
);



-- Добавляем пользователей
INSERT INTO [user] (username, password, role) VALUES 
('Чуча', '00000', 'admin'),
('Димон', '14068', 'courier'),
('Крипер', '31147', 'user'),
('Никита', '01010', 'manager');

-- Добавляем курьеров
INSERT INTO courier (name, is_active, old) VALUES 
('Богдан', 'True', 23),
('Славик', 'True', 30),
('Владислав', 'False', 18);

-- Добавляем категории
INSERT INTO categori (name) VALUES 
('KFC'),
('Subway'),
('Burger King'),
('Papa Doner');

-- Добавляем товары
INSERT INTO product (name, price, category_id) VALUES 
('Шаурма', 8, 4),
('Стрипсы', 6, 1),
('Сэндвич', 11, 2),
('Вопер', 5, 3),
('Соус', 3, 1),
('ещё что-то', 1, 2)

-- Добавляем заказы
INSERT INTO orders (user_id, product_id, courier_id, quantity, status) VALUES 
(3, 1, 1, 1, 'new'),
(3, 2, 1, 2, 'rejected'),
(3, 4, 2, 3, 'waiting'),
(2, 6, 2, 1, 'done'),
(4, 6, 2, 2, 'done');


SELECT 
    o.order_id,
    u.username AS client,
    p.name AS product,
    p.price,
    c.name AS restoran,
    cou.name AS courier,
    o.quantity,
    o.status,
    o.created_at
FROM orders o
JOIN [user] u ON o.user_id = u.user_id
JOIN product p ON o.product_id = p.product_id
JOIN categori c ON p.category_id = c.category_id
LEFT JOIN courier cou ON o.courier_id = cou.courier_id
ORDER BY o.created_at DESC;