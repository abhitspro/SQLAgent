-- 1. Create a read-only user
CREATE USER 'sql_agent_user'@'localhost' IDENTIFIED BY 'AgentSecurePassword123!';

-- 2. Grant SELECT-only privileges on your e-commerce database
GRANT SELECT ON ecommerce_agent_db.* TO 'sql_agent_user'@'localhost';

-- 3. Apply privilege changes
FLUSH PRIVILEGES;