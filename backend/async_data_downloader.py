from app.settings import logger
from app.queries import insert_data, check_record_exists
import aiomysql, asyncio, aiohttp, os
from flask import json
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv('DB_HOST')
USER = os.getenv('DB_USER')
PASSWORD = os.getenv('DB_PASSWORD')
DATABASE = os.getenv('DB_NAME')
PORT = int(os.getenv('DB_PORT', 3306))
API_KEY = os.getenv('API_KEY')
POP_STOCKS1 = ["AAPL", "MSFT", "GOOG", "GOOGL", "AMZN", "NVDA", "TSLA", "META", "JPM", "BAC", "WFC", "HD"]
POP_STOCKS2 = ["MCD", "NKE", "DIS", "JNJ", "UNH", "PFE", "XOM", "CVX", "TSM", "V", "UNP", "MA", "INTC"]
POP_STOCKS3 = ["CSCO", "ORCL", "IBM", "CRM", "ADBE", "PYPL", "NFLX", "T", "VZ", "CMCSA", "TMUS", "SBUX", "PEP"]

if not all([HOST, USER, PASSWORD, DATABASE, API_KEY]):
    logger.error('Missing environment variables.')
    exit(1)

async def fetch_data_and_insert(symbol, pool):
    async with aiohttp.ClientSession() as session:
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol={symbol}&apikey={API_KEY}'
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                data = await response.json()
                if 'Weekly Time Series' not in data:
                    logger.error(f'Invalid response from API for {symbol}')
                    return
                await process_data(pool, symbol, data['Weekly Time Series'])
                logger.info(f'Stock prices stored successfully for {symbol}')
        except aiohttp.ClientError as e:
            logger.error(f'API request failed for {symbol}: {e}')
        except json.JSONDecodeError as e:
            logger.error(f'Failed to decode JSON response for {symbol}: {e}')
        except KeyError as e:
            logger.error(f'Missing key in response: {symbol}: {e}')
        except ValueError as e:
            logger.error(f'Invalid value in API response for {symbol}: {e}')
        except Exception as e:
            logger.error(f'Failed to fetch data from the API for {symbol}: {e}')

async def process_data(pool, symbol, weekly_data):
    for date, values in weekly_data.items():
        try:
            open_price = values.get('1. open')
            high_price = values.get('2. high')
            low_price = values.get('3. low')
            close_price = values.get('4. close')
            volume = values.get('5. volume')
            if (not open_price or not close_price or not high_price or not low_price or not volume):
                logger.warning(f'Missing data for {symbol} on {date}')
                continue
            await insert_stock(pool, date, symbol, open_price, high_price, low_price, close_price, volume)
            logger.info(f'Inserted stock price for {symbol} on {date}')
        except Exception as e:
            logger.error(f'Error processing stock price for {symbol} on {date}: {e}')

async def insert_stock(pool, date_of_trade, stock_symbol, open_price, high_price, low_price, close_price, volume):
    connection = None
    try:
        async with pool.acquire() as connection:
            async with connection.cursor() as cursor:
                if not await record_exists(cursor, date_of_trade, stock_symbol, high_price, low_price, volume):
                    await cursor.execute(insert_data, (date_of_trade, stock_symbol, open_price, high_price, low_price, close_price, volume))
                    logger.info(f'Inserted stock price for {stock_symbol}.')
                else:
                    logger.info(f'Record for {stock_symbol} on {date_of_trade} already exists.')
            await connection.commit()
    except aiomysql.MySQLError as e:
        logger.error(f"Error inserting stock price: {e}")
        raise
    except Exception as e:
        logger.error(f"Error in insert_stock_price: {e}")

async def record_exists(cursor, date_of_trade, stock_symbol, high_price, low_price, volume):
    try:
        await cursor.execute(check_record_exists, (date_of_trade, stock_symbol, high_price, low_price, volume))
        result = await cursor.fetchone()
        if result is None:
            return False
        return result[0] > 0
    except Exception as e:
        logger.error(f"Error checking if record exists: {e}")
        raise Exception("Error checking if record exists") from e

async def create_async_pool():
    try:
        pool = await aiomysql.create_pool(
            host=HOST,
            user=USER,
            password=PASSWORD,
            db=DATABASE,
            port=PORT,
            autocommit=False,
            minsize=5,
            maxsize=10
        )
        logger.info("Connection pool created successfully")
        return pool
    except aiomysql.MySQLError as e:
        logger.error(f"Error creating connection pool: {e}")
        raise
    except Exception as e:
        logger.error(f"Error in create_connection_pool: {e}")
        raise

async def main():
    pool = await create_async_pool()
    if pool:
        try:
            tasks = [fetch_data_and_insert(symbol, pool) for symbol in POP_STOCKS1]
            await asyncio.gather(*tasks)
        finally:
            if pool:
                pool.close()
                await pool.wait_closed()
                logger.info("Connection pool closed successfully")