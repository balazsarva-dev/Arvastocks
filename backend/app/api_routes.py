from flask import Blueprint, jsonify, session, request, g
from app.settings import login_required_to_api, logger
from app.helper import fetch_data

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
    from app.sign_up_in import sign_up_user, registration_accepted_message
    import re

    data = request.json
    if not data:
        return jsonify({"message": "Invalid inputs. Please provide JSON data."}), 400

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"message": "Invalid inputs. All fields are required."}), 400

    if not re.match(r"^[a-zA-Z._%+-][a-zA-Z._%+-]*@[a-zA-Z-]+\.[a-zA-Z]{2,}$", email):
        return jsonify({"message": "Invalid email address."}), 400

    signed_up_user = sign_up_user(username, password, email)
    if signed_up_user:
        return jsonify({"message": "User registered successfully!"}), 200
    else:
        return jsonify({"message": "Failed to register user!"}), 500


@api.route('/login', methods=['POST'])
def login():
    from app.sign_up_in import authenticate_user

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
    from app.sign_up_in import delete_user_from_db
    
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
        news = fetch_data(symbol, news=True)
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
    candlestick_setting = data.get("candlestick_setting", True)

    if not symbol:
        return jsonify({"message": "Invalid inputs. Stock symbol is required."}), 400

    try:
        figure = plot_helper(symbol, candlestick_setting)
        return jsonify({"figure": figure}), 200
    except Exception as e:
        logger.error(f"Error generating candlestick chart: {e}")
        return jsonify({"error": "Failed to generate candlestick chart"}), 500

def plot_helper(symbol, candlestick_setting: bool = True):
    from app.queries import select_data_by_symbol
    from app.helper import plotting_stock_prices
    from app.db import get_connection, release_connection
    from app.settings import logger
    
    connection = None
    try:
        connection = get_connection()
        if connection:
            try:
                with connection.cursor() as cursor:
                    logger.debug(f"Fetching data for symbol: {symbol}")
                    cursor.execute(select_data_by_symbol, (symbol,))
                    data = cursor.fetchall()
                    logger.debug(f"Fetched data: {data}")
                return plotting_stock_prices(data, symbol, candlestick=candlestick_setting)
            except Exception as e:
                return str(e)
            finally:
                if connection:
                    release_connection(connection)
        else:
            return "Database connection not available."
    except Exception as e:
        return str(e)

@api.route("/contact", methods=["POST"])
def contact():
    from app.sign_up_in import send_contact_email

    try:
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
        email_sent = send_contact_email(name, email, message)

        if email_sent:
            logger.info("Email sent successfully.")
            return jsonify({"message": "Email sent successfully!"}), 200
        else:
            logger.error("Failed to send email.")
            return jsonify({"message": "Failed to send email!"}), 500
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return jsonify({"message": "An internal server error occurred."}), 500


@api.route("/update_user_password", methods=["POST"])
@login_required_to_api
def update_user_password():
    from app.sign_up_in import update_password

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
    from app.sign_up_in import update_email

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
