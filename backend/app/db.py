from app.settings import logger, log_execution
from app.queries import (
    create_stocks_new_table,
    create_users_table,
    insert_data,
    check_record_exists,
)
import time

MAX_RETRIES = 5
INITIAL_DELAY = 2
MAX_RETRY_DELAY = 30


@log_execution
def get_connection():
    from app import app

    logger.info("Connecting to the database...")
    for attempt in range(MAX_RETRIES):
        retry_delay = min(INITIAL_DELAY * (2 ** attempt), MAX_RETRY_DELAY)
        try:
            if app.db_pool is None:
                logger.error("Database pool not created.")
                logger.info("Retrying in %d seconds...", retry_delay)
                time.sleep(retry_delay)
                continue
            conn = app.db_pool.connection()
            logger.info("Database connection successful.")
            return conn
        except Exception as e:
            logger.error(f"Error connecting to the database: {e}")
            logger.info("Retrying in %d seconds...", retry_delay)
            time.sleep(retry_delay)
    logger.critical("Max retries reached. Unable to connect to the database.")
    return None


@log_execution
def release_connection(conn):
    from app import app

    try:
        if conn:
            app.db_pool.close()
            logger.info("Database connection released to the pool.")
    except Exception as e:
        logger.error(f"Error releasing database connection: {e}")


@log_execution
def init_db(app):
    logger.info("Initializing the database...")
    connection = None
    try:
        connection = get_connection()
        if connection:
            try:
                with connection.cursor() as cursor:
                    for command in [create_stocks_new_table, create_users_table]:
                        cursor.execute(command)
                connection.commit()
                logger.info("Table 'stocks' and 'users' created successfully")
            finally:
                if connection:
                    release_connection(connection)
        else:
            logger.error("Database connection not available.")
    except Exception as e:
        logger.error(f"Error initializing the database: {e}")
        raise e


@log_execution
def record_exists(cursor, date_of_trade, stock_symbol, high_price, low_price, volume):
    cursor.execute(check_record_exists, (date_of_trade, stock_symbol, high_price, low_price, volume))
    return cursor.fetchone()["count"] > 0


@log_execution
def insert_stock_price(
    cursor,
    date_of_trade,
    stock_symbol,
    open_price,
    high_price,
    low_price,
    close_price,
    volume,
):
    if not record_exists(cursor, date_of_trade, stock_symbol, high_price, low_price, volume):
        cursor.execute(
            insert_data,
            (
                date_of_trade,
                stock_symbol,
                open_price,
                high_price,
                low_price,
                close_price,
                volume,
            ),
        )
        logger.info(f"Inserted stock price for {stock_symbol}.")
    else:
        logger.info(f"Record for {stock_symbol} on {date_of_trade} already exists.")
