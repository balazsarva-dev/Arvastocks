from flask import Blueprint, jsonify, session, request, g
from app.settings import login_required_to_api, logger
from app.helper import fetch_data_from_api
from app.sign_up_in import (
                            sign_up_user,
                            send_email_via_sendgrid,
                            send_registration_email,
                            authenticate_user, 
                            delete_user_from_db,
                            update_email, 
                            update_password
)
from app import app
import re
from threading import Thread


api = Blueprint("api", __name__)

@api.before_request
def load_logged_in_user():
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
        return

    from app.db import get_connection, release_connection
    from app.queries import check_user_exists_by_id

    connection = None
    try:
        connection = get_connection()
        if connection:
            with connection.cursor() as cursor:
                cursor.execute(check_user_exists_by_id, (user_id,))
                g.user = cursor.fetchone()
        else:
            g.user = None
    except Exception as e:
        g.user = None
    finally:
        if connection:
            release_connection(connection)

@api.route("/")
def home():
    return jsonify({"message": "Welcome to the Arvastocks API!"}), 200

@api.route("/register", methods=["POST"])
def register():
    data = request.json
    if not data:
        return jsonify({"message": "Invalid inputs. Please provide JSON data."}), 400

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"message": "Invalid inputs. All fields are required."}), 400

    if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
        return jsonify({"message": "Invalid email address."}), 400

    signed_up_user = sign_up_user(username, password, email)
    if signed_up_user:        
        thread = Thread(target=send_registration_email, args=(email, username))
        thread.start()
        logger.info(f"Sent welcome email to {email}")
        return jsonify({"message": "User registered, and sent welcome email!"}), 200
    else:
        return jsonify({"message": "Failed to register user!"}), 500

@api.route('/login', methods=['POST'])
def login():
    data = request.json
    if not data:
        return jsonify({"message": "Invalid inputs. Please provide JSON data."}), 400

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"message": "Invalid inputs. All fields are required."}), 400

    auth_result = authenticate_user(username, password)
    if auth_result["success"]:
        user = auth_result["user"]
        session["user_id"] = user["id"]
        session["username"] = user["username"]
        session["email"] = user["email"]
        return jsonify({
            "success": True,
            "username": session['username'],
            "email": session['email'],
            "message": "Signed in successfully!"
        }), 200
    else:
        return jsonify({
            "success": False,
            "message": auth_result["error"]
        }), 401

@api.route('/logout', methods=['POST'])
@login_required_to_api
def logout():
    session.clear()
    g.user = None
    return jsonify({"message": "Signed out successfully!"}), 200

@api.route('/profile', methods=['GET'])
@login_required_to_api
def profile():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify({
        "username": session.get("username"),
        "email": session.get("email")
    }), 200

@api.route('/delete_user', methods=['POST'])
@login_required_to_api
def delete_user():
    data = request.json
    if not data:
        return jsonify({"message": "Invalid inputs. Please provide JSON data."}), 400

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"message": "Invalid inputs. All fields are required."}), 400

    deleted_user = delete_user_from_db(username, email, password)
    if deleted_user:
        session.clear()
        return jsonify({"message": "User deleted successfully!"}), 200
    else:
        return jsonify({"message": "Failed to delete user!"}), 500

@api.route('/news_data', methods=['GET'])
def news_data():
    symbol = request.args.get("symbol")
    logger.debug(f"Received request for symbol: {symbol}")
    if not symbol:
        logger.debug("No stock symbol provided")
        return jsonify({"error": "Stock symbol is required"}), 400
    try:
        news = fetch_data_from_api(symbol, news=True)
        logger.debug(f"Fetched news: {news}")
        if news:
            return jsonify(news), 200
        else:
            logger.debug("No news found for the given stock symbol")
            return jsonify({"error": "No news found for the given stock symbol"}), 404
    except Exception as e:
        logger.error(f"Error fetching news data: {e}")
        return jsonify({"error": "An error occurred while fetching news data"}), 500
    
@api.route("/candlestick", methods=["POST"])
def candlestick():
    data = request.json
    if not data:
        logger.error("No JSON data provided in the request.")
        return jsonify({"message": "Invalid inputs. Please provide JSON data."}), 400

    symbol = data.get("symbol")

    if not symbol:
        return jsonify({"message": "Invalid inputs. Stock symbol is required."}), 400

    try:
        figure = plot_helper(symbol)
        if not figure:
            logger.error("No data found for the given stock symbol.")
            return jsonify({"error": "No data found for the given stock symbol"}), 404
        return jsonify(figure), 200
    except Exception as e:
        logger.error(f"Error generating candlestick chart: {e}")
        return jsonify({"error": "Failed to generate candlestick chart"}), 500

def plot_helper(symbol):
    from app.queries import select_data_by_symbol
    from app.db import get_connection, release_connection
    
    connection = None
    try:
        connection = get_connection()
        if not connection:
            logger.error("Database connection not available.")
            raise Exception("Database connection not available.")
        with connection.cursor() as cursor:
            logger.debug(f"Fetching data for symbol: {symbol}")
            cursor.execute(select_data_by_symbol, (symbol,))
            data = cursor.fetchall()
            logger.debug(f"Fetched data: {len(data)} rows for symbol: {symbol}")
            return validate_data(data, symbol)
    except Exception as e:
        logger.error(f"Error fetching data for symbol {symbol}: {e}")
        raise
    finally:
        if connection:
            release_connection(connection)

def validate_data(data, symbol):
    if not data:
        logger.info(f"No data found for symbol: {symbol}")
        return []
    stocks = []
    for row in data:
        try:
            stocks.append({
                "x": row["date_of_trade"].isoformat() if row["date_of_trade"] else None,
                "o": float(row["open_price"]) if row["open_price"] is not None else 0.0,
                "h": float(row["high_price"]) if row["high_price"] is not None else 0.0,
                "l": float(row["low_price"]) if row["low_price"] is not None else 0.0,
                "c": float(row["close_price"]) if row["close_price"] is not None else 0.0,
            })
        except Exception as e:
            logger.error(f"Error processing row: {row}, Error: {e}")
            continue
    logger.info(f"Processed data for symbol: {symbol}, Stocks: {stocks}")
    return stocks


@api.route("/contact", methods=["POST"])
def contact():
    data = request.json
    if not data:
        logger.error("No JSON data provided in the request.")
        return jsonify({"message": "Invalid inputs. Please provide JSON data."}), 400

    name = data.get("name")
    email = data.get("email")
    message = data.get("message")

    if not name or not email or not message:
        logger.error("Missing required fields: name, email, or message.")
        return jsonify({"message": "Invalid inputs. All fields are required."}), 400

    logger.info(f"Attempting to send email with name: {name}, email: {email}, message: {message}")
    subject = "Contact Form Submission"
    body = f"Name: {name}\nEmail: {email}\nMessage: {message}"
    from_email = app.config["MAIL_DEFAULT_SENDER"]
    to_email = app.config["MAIL_DEFAULT_SENDER"]

    thread = Thread(target=send_email_via_sendgrid, args=(subject, body, from_email, to_email))
    thread.start()
    logger.info(f"Sent contact email to {to_email} from {from_email}")
    return jsonify({"message": "Email sent successfully!"}), 200

@api.route("/update_user_password", methods=["POST"])
@login_required_to_api
def update_user_password():
    data = request.json
    if not data:
        return jsonify({"message": "Invalid inputs. Please provide JSON data."}), 400

    old_password = data.get("old_password")
    new_password = data.get("new_password")

    if not old_password or not new_password:
        return jsonify({"message": "Invalid inputs. All fields are required."}), 400

    username = g.user["username"]
    password_updated = update_password(username, old_password, new_password)
    if password_updated:
        return jsonify({"message": "Password updated successfully!"}), 200
    else:
        return jsonify({"message": "Failed to update password!"}), 500

@api.route("/update_user_email", methods=["POST"])
@login_required_to_api
def update_user_email():
    data = request.json
    if not data:
        return jsonify({"message": "Invalid inputs. Please provide JSON data."}), 400

    new_email = data.get("new_email")
    password = data.get("password")

    if not new_email or not password:
        return jsonify({"message": "Invalid inputs. All fields are required."}), 400

    username = g.user["username"]
    email_updated = update_email(username, new_email, password)
    if email_updated:
        return jsonify({"message": "Email changed successfully!"}), 200
    else:
        return jsonify({"message": "Failed to change email!"}), 500
