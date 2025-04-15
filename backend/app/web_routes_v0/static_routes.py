# from app.settings import logger, login_required
# from app.db import get_connection, release_connection
# from app.queries import check_user_exists_by_id
# from app.sign_up_in import send_contact_email
# from flask import jsonify, request, render_template, flash, session, redirect, url_for, g
# from app.forms import ContactForm
# from app import app
# from app.helper import fetch_news


# # @app.before_request
# # def load_logged_in_user():
# #     logger.info("Loading logged in user...")
# #     user_id = session.get("user_id")
# #     if user_id is None:
# #         g.user = None
# #         logger.info("No user_id in session")
# #         return

# #     connection = None
# #     try:
# #         connection = get_connection()
# #         if connection:
# #             with connection.cursor() as cursor:
# #                 cursor.execute(check_user_exists_by_id, (user_id,))
# #                 g.user = cursor.fetchone()
# #                 logger.info(f"User loaded: {g.user}")
# #         else:
# #             logger.error("Database connection not available")
# #             g.user = None
# #     except Exception as e:
# #         logger.error(f"Error loading user: {e}")
# #         g.user = None
# #     finally:
# #         if connection:
# #             release_connection(connection)


# # @app.route("/")
# # def home():
# #     username = session.get("username")
# #     return render_template("index.html", username=username)


# # @app.route("/about")
# # def about():
# #     return render_template("about.html")


# @app.route("/terms")
# def terms():
#     return render_template("terms.html")


# @app.route("/contact", methods=["GET", "POST"])
# def contact():
#     form = ContactForm()
#     if request.method == "POST":
#         if form.validate_on_submit():
#             name = form.name.data
#             email = form.email.data
#             message = form.message.data
#             email_sent = send_contact_email(name, email, message)
#             if email_sent:
#                 flash("Message sent successfully! ", "success")
#                 return redirect(url_for("home"))
#             else:
#                 flash("Failed to send message! ", "error")
#     return render_template("contact.html", form=form)


# @app.route("/dashboard")
# @login_required
# def dashboard():
#     return render_template("dashboard.html")

# @app.route("/news")
# def news():
#     return render_template("news.html")

# @app.route("/news_data", methods=["GET"])
# def news_data():
#     symbol = request.args.get("symbol")
#     if not symbol:
#         return jsonify({"error": "Stock symbol is required"}), 400
#     try:
#         news_data = fetch_news(symbol)
#         if not news_data:
#             return jsonify({"error": "No news data found"}), 404
#         return jsonify(news_data)
#     except Exception as e:
#         logger.error(f"Error fetching news data: {e}")
#         return jsonify({"error": "Failed to fetch news data"}), 500