-- Categories
INSERT INTO categories (category_name) VALUES 
('Electronics'), 
('Clothing'), 
('Home & Kitchen'), 
('Books');

-- Products
INSERT INTO products (product_name, category_id, price, stock_quantity) VALUES 
('Wireless Noise-Canceling Headphones', 1, 199.99, 45),
('Mechanical Gaming Keyboard', 1, 89.50, 30),
('Cotton Crewneck T-Shirt', 2, 19.99, 120),
('Denim Jeans', 2, 49.99, 80),
('Stainless Steel Coffee Maker', 3, 79.90, 15),
('Non-Stick Frying Pan', 3, 29.99, 60),
('Designing Data-Intensive Applications', 4, 42.00, 25),
('Clean Code', 4, 38.50, 40);

-- Customers
INSERT INTO customers (first_name, last_name, email, city, country) VALUES 
('Aarav', 'Sharma', 'aarav.sharma@example.com', 'Mumbai', 'India'),
('Sophia', 'Chen', 'sophia.chen@example.com', 'Toronto', 'Canada'),
('Liam', 'Smith', 'liam.smith@example.com', 'New York', 'USA'),
('Emma', 'Watson', 'emma.watson@example.com', 'London', 'UK');

-- Orders
INSERT INTO orders (customer_id, order_date, status, total_amount) VALUES 
(1, '2026-02-10 10:30:00', 'Delivered', 289.49),
(2, '2026-02-15 14:20:00', 'Shipped', 119.89),
(3, '2026-03-01 09:15:00', 'Delivered', 42.00),
(1, '2026-03-05 18:45:00', 'Pending', 79.90),
(4, '2026-03-12 11:00:00', 'Cancelled', 49.99);

-- Order Items
INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES 
(1, 1, 1, 199.99),
(1, 2, 1, 89.50),
(2, 3, 1, 19.99),
(2, 5, 1, 79.90),
(3, 7, 1, 42.00),
(4, 5, 1, 79.90),
(5, 4, 1, 49.99);