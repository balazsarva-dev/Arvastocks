import os, requests
from ratelimit import limits, sleep_and_retry
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)
import plotly.graph_objects as go
from app.settings import logger
from app.db import get_connection, insert_stock_price, release_connection

CALLS = 5
PERIOD = 60

def is_rate_limit_exception(exception):
    return (
        isinstance(exception, requests.exceptions.HTTPError)
        and exception.response.status_code == 429
    )


@sleep_and_retry
@limits(calls=CALLS, period=PERIOD)
@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=4, max=60),
    retry=retry_if_exception_type(is_rate_limit_exception),
)
def fetch_data_from_api(symbol, apikey):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol={symbol}&apikey="
    endpoint = url + apikey
    response = requests.get(endpoint)
    data = response.json()
    logger.debug(f"Response completed with status code {response.status_code}")
    return data


def fetch_news(symbol):
    url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={symbol}&apikey="
    apikey = os.getenv("API_KEY")
    if not apikey:
        raise ValueError("API_KEY is required")
    endpoint = url + apikey
    response = requests.get(endpoint)
    data = response.json()
    logger.debug(f"Response completed with status code {response.status_code}")
    return data


def fetch_data(symbol):
    if not symbol:
        raise ValueError("Symbol is required")
    apikey = os.getenv("API_KEY")
    if not apikey:
        raise ValueError("API_KEY is required")
    try:
        return fetch_data_from_api(symbol, apikey)
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {e}")
        raise ValueError("Failed to fetch data from the API") from e
    except Exception as e:
        logger.error("No weekly data found in the response")
        raise ValueError("Failed to process the response") from e


def process_weekly_data(cursor, symbol, weekly_data):
    for date, values in weekly_data.items():
        try:
            open_price = values.get("1. open")
            high_price = values.get("2. high")
            low_price = values.get("3. low")
            close_price = values.get("4. close")
            volume = values.get("5. volume")

            if (
                not open_price
                or not close_price
                or not high_price
                or not low_price
                or not volume
            ):
                logger.warning(f"No stock price found for {symbol} on {date}")
                continue
            if not is_valid_price(open_price, high_price, low_price, close_price):
                logger.error(f"Invalid stock price format for {symbol} on {date}")
                continue
            stock_data = [open_price, high_price, low_price, close_price, volume]
            insert_stock_price(cursor, date, symbol, *stock_data)
            logger.info(f"Inserted stock price for {symbol} on {date}")
        except Exception as e:
            logger.error(f"Error processing stock price for {symbol} on {date}: {e}")
            continue


def store_data(symbol, data):
    if "Weekly Time Series" not in data:
        raise ValueError("Invalid response from API")
    weekly_data = data["Weekly Time Series"]
    connection = None
    try:
        connection = get_connection()
        if connection:
            try:
                with connection.cursor() as cursor:
                    process_weekly_data(cursor, symbol, weekly_data)
                connection.commit()
                return {"message": "Stock prices stored successfully"}
            except Exception as e:
                logger.error(f"Error storing data for {symbol}: {e}")
                raise ValueError("Failed to store data in the database") from e
            finally:
                if connection:
                    release_connection(connection)
    except Exception as e:
        logger.error(f"Error storing data for {symbol}: {e}")
        raise ValueError("Failed to store data in the database") from e


def is_valid_price(open_price, high_price, low_price, close_price):
    try:
        open_price = float(open_price)
        high_price = float(high_price)
        low_price = float(low_price)
        close_price = float(close_price)
    except ValueError:
        logger.error("Invalid stock price format")
        return False
    if open_price < 0 or open_price > 10000 or close_price < 0 or close_price > 10000:
        logger.error("Stock price out of range")
        return False
    return True


def background_task(symbol):
    data = fetch_data(symbol)
    if not data:
        logger.error("Data is required")
        return
    return store_data(symbol, data)


def plotting_stock_prices(data, symbol, candlestick: bool = True):
    dates = [row["date_of_trade"] for row in data]
    open_prices = [float(row["open_price"]) for row in data]
    high_prices = [float(row["high_price"]) for row in data]
    low_prices = [float(row["low_price"]) for row in data]
    close_prices = [float(row["close_price"]) for row in data]
    fig = go.Figure()
    if candlestick is False:
        fig.add_trace(
            go.Scatter(x=dates, y=close_prices, mode="lines", name="Close Price")
        )
        fig.add_trace(
            go.Scatter(x=dates, y=open_prices, mode="lines", name="Open Price")
        )
    fig.add_trace(
        go.Candlestick(
            x=dates,
            open=open_prices,
            high=high_prices,
            low=low_prices,
            close=close_prices,
        )
    )
    fig.update_layout(
        title=f"{symbol} Stock Price",
        xaxis_title="Date",
        yaxis_title="Price",
        xaxis_rangeslider_visible=False,
    )
    return fig.to_html(full_html=False)
