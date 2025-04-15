create_stocks_new_table = """
                    CREATE TABLE IF NOT EXISTS stocks_new (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            date_of_trade DATE,
                            stock_symbol VARCHAR(10),
                            open_price DECIMAL(18, 2),
                            high_price DECIMAL(18, 2),
                            low_price DECIMAL(18, 2),
                            close_price DECIMAL(18, 2),
                            volume BIGINT
                        );
                        """

create_users_table = """
                    CREATE TABLE IF NOT EXISTS users (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            username VARCHAR(50) UNIQUE,
                            password VARCHAR(255),
                            email VARCHAR(50) UNIQUE
                        );
                        """

select_data_by_symbol = """
                    SELECT date_of_trade, open_price, high_price, low_price, close_price
                    FROM stocks_new
                    WHERE stock_symbol = %s
                    ORDER BY date_of_trade DESC
                    """

insert_data = """
                    INSERT INTO stocks_new
                    (date_of_trade, stock_symbol, open_price, high_price, low_price, close_price, volume) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """

check_record_exists = """
                    SELECT COUNT(*) AS count
                    FROM stocks_new 
                    WHERE date_of_trade = %s AND stock_symbol = %s AND high_price = %s AND low_price = %s AND volume = %s
                    """

check_user_exists = """
                    SELECT id, username, password, email FROM users
                    WHERE username = %s OR email = %s
                    """

check_user_exists_by_id = """
                    SELECT id, username, password, email FROM users
                    WHERE id = %s
                    """

check_user_exists_by_username = """
                    SELECT id, username, password, email FROM users
                    WHERE username = %s
                    """

insert_user = """
                    INSERT INTO users
                    (username, password, email)
                    VALUES (%s, %s, %s)
                    """

delete_user = """
                    DELETE FROM users
                    WHERE username = %s AND email = %s
                    """

update_user_password = """
                    UPDATE users
                    SET password = %s
                    WHERE username = %s
                    """

update_user_email = """
                    UPDATE users
                    SET email = %s
                    WHERE username = %s
                    """
