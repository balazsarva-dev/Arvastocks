# import threading
# from app import app, cache
# from app.settings import login_required, logger
# from app.db import get_connection, release_connection
# from app.helper import background_task, plotting_stock_prices
# from app.queries import select_data_by_symbol
# from flask import request, render_template, flash
# import pandas as pd


# @app.route("/stock_data")
# @login_required
# def stock_data():
#     symbol = request.args.get("symbol")
#     if not symbol:
#         return render_template("stock_data.html", error="Stock symbol is required")

#     connection = None
#     try:
#         connection = get_connection()
#         if connection:
#             try:
#                 with connection.cursor() as cursor:
#                     cursor.execute(select_data_by_symbol, (symbol,))
#                     data = cursor.fetchall()
#                 return extracted_from_stock_data(symbol, data)
#             except Exception as e:
#                 return render_template("stock_data.html", error=str(e))
#             finally:
#                 if connection:
#                     release_connection(connection)
#         else:
#             return render_template("stock_data.html", error="Database connection not available.")
#     except Exception as e:
#         return render_template("stock_data.html", error=str(e))

# def extracted_from_stock_data(symbol, data):
#     if not data:
#         flash(f"No data found for {symbol}. Please wait for the data to be stored", "info")
#         thread = threading.Thread(target=background_task, args=(symbol,))
#         thread.start()
#         return render_template("stock_data.html", symbol=symbol)
#     df = pd.DataFrame(data)
#     html_table = df.to_html(classes="table table-striped table-bordered table-hover")
#     return render_template("stock_data.html", symbol=symbol, table=html_table)


# def plot_helper(symbol, candlestick_setting: bool = True):
#     from app.queries import select_data_by_symbol
#     from app.helper import plotting_stock_prices
#     from app.db import get_connection, release_connection
#     from app.settings import logger
    
#     connection = None
#     try:
#         connection = get_connection()
#         if connection:
#             try:
#                 with connection.cursor() as cursor:
#                     logger.debug(f"Fetching data for symbol: {symbol}")
#                     cursor.execute(select_data_by_symbol, (symbol,))
#                     data = cursor.fetchall()
#                     logger.debug(f"Fetched data: {data}")
#                 return plotting_stock_prices(data, symbol, candlestick=candlestick_setting)
#             except Exception as e:
#                 return str(e)
#             finally:
#                 if connection:
#                     release_connection(connection)
#         else:
#             return "Database connection not available."
#     except Exception as e:
#         return str(e)


# @app.route("/candlestick_chart/<symbol>")
# @login_required
# @cache.cached(timeout=60)
# def candlestick_chart(symbol):
#     return plot_helper(symbol, candlestick_setting=True)


# @app.route("/line_chart/<symbol>")
# @login_required
# @cache.cached(timeout=60)
# def line_chart(symbol):
#     return plot_helper(symbol, candlestick_setting=False)
