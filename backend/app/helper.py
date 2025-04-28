import os, requests
from ratelimit import limits, sleep_and_retry
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import plotly.graph_objects as go
from app.settings import logger

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
def fetch_data_from_api(symbol, apikey=os.getenv("API_KEY"), news: bool = False):
    if news is True:
        url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={symbol}&apikey="
    else:
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol={symbol}&apikey="
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
