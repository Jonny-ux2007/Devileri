CREATE DATABASE Food;
GO

USE Food;
GO

-- 1. Удаляем старые таблицы, если они есть
IF OBJECT_ID('order_items', 'U') IS NOT NULL DROP TABLE order_items;
IF OBJECT_ID('orders', 'U') IS NOT NULL DROP TABLE orders;
IF OBJECT_ID('product', 'U') IS NOT NULL DROP TABLE product;
IF OBJECT_ID('categori', 'U') IS NOT NULL DROP TABLE categori;
IF OBJECT_ID('courier', 'U') IS NOT NULL DROP TABLE courier;
IF OBJECT_ID('user', 'U') IS NOT NULL DROP TABLE [user];
GO

-- 2. Создаем таблицы
CREATE TABLE [user] (
    user_id INT IDENTITY(1,1) PRIMARY KEY,
    username NVARCHAR(50) NOT NULL UNIQUE,
    password NVARCHAR(255) NOT NULL,
    role NVARCHAR(20) NOT NULL CHECK(role IN ('user', 'admin', 'manager', 'courier')) DEFAULT 'user',
    created_at DATETIME DEFAULT GETDATE()
);

CREATE TABLE courier (
    courier_id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(100) NOT NULL,
    is_active NVARCHAR(10) NOT NULL DEFAULT 'True',
    old INT CHECK(old BETWEEN 16 AND 50),
    created_at DATETIME DEFAULT GETDATE()
);

CREATE TABLE categori (
    category_id INT IDENTITY(1,1) PRIMARY KEY,
    name_category NVARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE product (
    product_id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(100) NOT NULL UNIQUE,
    price DECIMAL(10,2) NOT NULL CHECK(price > 0),
    category_id INT NOT NULL,
    CONSTRAINT FK_product_categori FOREIGN KEY (category_id) REFERENCES categori(category_id)
);

CREATE TABLE orders (
    order_id INT IDENTITY(1,1) PRIMARY KEY,
    user_id INT NOT NULL,
    courier_id INT NULL,
    status NVARCHAR(20) NOT NULL CHECK(status IN ('new', 'waiting', 'done', 'rejected')) DEFAULT 'new',
    created_at DATETIME DEFAULT GETDATE(),
    CONSTRAINT FK_orders_user FOREIGN KEY (user_id) REFERENCES [user](user_id),
    CONSTRAINT FK_orders_courier FOREIGN KEY (courier_id) REFERENCES courier(courier_id)
);

CREATE TABLE order_items (
    item_id INT IDENTITY(1,1) PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    price_one_order INT NOT NULL,
    CONSTRAINT FK_items_orders FOREIGN KEY (order_id) REFERENCES orders(order_id),
    CONSTRAINT FK_items_product FOREIGN KEY (product_id) REFERENCES product(product_id)
);
GO

-- 3. Заполняем данные
INSERT INTO [user] (username, password, role) VALUES
('Чуча', '00000', 'admin'),
('Димон', '14068', 'courier'),
('Крипер', '31147', 'user'),
('Никита', '01010', 'manager');

INSERT INTO courier (name, is_active, old) VALUES
('Богдан', 'True', 23),
('Славик', 'True', 30),
('Владислав', 'False', 18);

INSERT INTO categori (name_category) VALUES
('Напитки'),
('Картошка'),
('Донеры'),
('Соусы');

INSERT INTO product (name, price, category_id) VALUES
('Средняя картошка', 8, 2),
('Coca-Cola', 6, 1),
('Донер Чизер', 11, 3),
('Донер Чикен', 5, 3),
('Сырный соус', 3, 4);

INSERT INTO orders (user_id, courier_id, status) VALUES
(3, 1, 'new'),
(3, 1, 'rejected'),
(3, 2, 'waiting'),
(2, 2, 'done'),
(4, 2, 'done');

INSERT INTO order_items (order_id, product_id, price_one_order) VALUES
(1, 1, 8),
(1, 2, 6),
(2, 2, 6),
(3, 4, 5),
(4, 5, 3),
(5, 5, 3);
GO

-- 4. Выводим отчет
SELECT
    o.order_id,
    u.username AS client,
    p.name AS product,
    p.price,
    c.name_category AS category,
    cou.name AS courier,
    o.status,
    o.created_at
FROM orders o
JOIN [user] u ON o.user_id = u.user_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN product p ON oi.product_id = p.product_id
JOIN categori c ON p.category_id = c.category_id
LEFT JOIN courier cou ON o.courier_id = cou.courier_id
ORDER BY o.created_at DESC;
GO