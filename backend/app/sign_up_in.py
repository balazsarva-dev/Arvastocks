from app.queries import (
    check_user_exists,
    check_user_exists_by_username,
    insert_user,
    delete_user,
    update_user_password,
    update_user_email,
)
from app.db import get_connection, release_connection
from app.settings import logger
from app import mail
from flask import session
from flask_mail import Message
from bcrypt import hashpw, checkpw, gensalt
import os


def sign_up_user(username, password, email):
    connection = None
    try:
        connection = get_connection()
        if connection:
            try:
                with connection.cursor() as cursor:
                    cursor.execute(check_user_exists, (username, email))
                    user = cursor.fetchone()
                    user_exists = True if user else False
                    if user_exists:
                        return False
                    else:
                        password = hashpw(password.encode("utf-8"), gensalt()).decode(
                            "utf-8"
                        )
                        cursor.execute(insert_user, (username, password, email))
                        connection.commit()
                        return True
            except Exception as e:
                logger.error(f"Error registering user: {e}")
                return False
            finally:
                if connection:
                    release_connection(connection)
    except Exception as e:
        logger.error(f"Error registering user: {e}")
        return False


def authenticate_user(username, password):
    connection = None
    try:
        connection = get_connection()
        if connection:
            try:
                with connection.cursor() as cursor:
                    cursor.execute(check_user_exists_by_username, (username,))
                    user = cursor.fetchone()
                    if not user:
                        logger.warning("User not found")
                        return {"success": False, "error": "User not found"}
                    if not checkpw(password.encode("utf-8"), user["password"].encode("utf-8")):
                        logger.warning("Invalid password")
                        return {"success": False, "error": "Invalid password"}
                    
                    # Set session variables
                    session["user_id"] = user["id"]
                    session["username"] = user["username"]
                    session["email"] = user["email"]
                    return {"success": True, "user": user}
            except Exception as e:
                logger.error(f"Error signing in: {e}")
                return {"success": False, "error": "Internal server error"}
            finally:
                if connection:
                    release_connection(connection)
    except Exception as e:
        logger.error(f"Error signing in: {e}")
        return {"success": False, "error": "Internal server error"}


def send_contact_email(name, email, message):
    try:
        msg = Message(
            "New message from your website",
            sender=os.getenv("MAIL_DEFAULT_SENDER"),
            recipients=[os.getenv("MAIL_DEFAULT_SENDER")],
        )
        msg.body = f"Name: {name}\nEmail: {email}\n\n{message}"
        msg.subject = f"Contact from {name}"
        mail.send(msg)
        return True
    except Exception as e:
        logger.error(f"Error sending message: {e}")
        return False


def delete_user_from_db(username, email):
    connection = None
    try:
        connection = get_connection()
        if connection:
            try:
                with connection.cursor() as cursor:
                    cursor.execute(delete_user, (username, email))
                    connection.commit()
                    session.clear()
                    return True
            except Exception as e:
                logger.error(f"Error deleting user: {e}")
                return False
            finally:
                if connection:
                    release_connection(connection)
    except Exception as e:
        logger.error(f"Error deleting user: {e}")
        return False


def registration_accepted_message(username, email):
    try:
        msg = Message(
            "Welcome to the Stock Price App",
            sender=os.getenv("MAIL_DEFAULT_SENDER"),
            recipients=[email],
        )
        msg.body = f"Dear {username},\n\nThank you for registering with us. We hope you enjoy our services.\
            \nPlease do not hesitate to contact us if you have any questions.\n\nBest regards,\nThe Stock Price App Team"
        msg.subject = "Welcome to the Stock Price App"
        mail.send(msg)
        return True
    except Exception as e:
        logger.error(f"Error sending registration message: {e}")
        return False


def update_password(username, old_password, new_password):
    verification = verify_password(username, old_password)
    if not verification:
        return False
    connection = None
    try:
        connection = get_connection()
        if connection:
            try:
                with connection.cursor() as cursor:
                    new_password = hashpw(
                        new_password.encode("utf-8"), gensalt()
                    ).decode("utf-8")
                    cursor.execute(update_user_password, (new_password, username))
                    connection.commit()
                    return True
            except Exception as e:
                logger.error(f"Error updating password: {e}")
                return False
            finally:
                if connection:
                    release_connection(connection)
    except Exception as e:
        logger.error(f"Error updating password: {e}")
        return False


def update_email(username, new_email, password):
    logger.info(f"Updating email for {username} to {new_email}")
    verification = verify_password(username, password)
    if not verification:
        logger.warning("Password verification failed")
        return False
    connection = None
    try:
        connection = get_connection()
        if connection:
            try:
                with connection.cursor() as cursor:
                    logger.info(f"Updating email for {username} to {new_email}")
                    cursor.execute(update_user_email, (new_email, username))
                    connection.commit()
                    logger.info(f"Email updated for {username} to {new_email}")
                    return True
            except Exception as e:
                logger.error(f"Error updating email: {e}")
                return False
            finally:
                if connection:
                    release_connection(connection)
    except Exception as e:
        logger.error(f"Error updating email: {e}")
        return False


def verify_password(username, old_password):
    logger.info(f"Verifying password for {username}")
    connection = None
    try:
        connection = get_connection()
        if connection:
            try:
                with connection.cursor() as cursor:
                    cursor.execute(check_user_exists_by_username, (username,))
                    user = cursor.fetchone()
                    if not user:
                        logger.warning(f"User {username} not found")
                        return False
                    if not checkpw(old_password.encode("utf-8"), user["password"].encode("utf-8")):
                        logger.warning(f"Password verification failed for {username}")
                        return False
                    return True
            except Exception as e:
                logger.error(f"Error verifying password: {e}")
                return False
            finally:
                if connection:
                    release_connection(connection)
    except Exception as e:
        logger.error(f"Error verifying password: {e}")
        return False


#Delete function to api endpoint

def delete_user_from_db_to_api(username, email, password):
    connection = None
    try:
        connection = get_connection()
        if connection:
            try:
                with connection.cursor() as cursor:
                    cursor.execute(check_user_exists_by_username, (username,))
                    user = cursor.fetchone()
                    if not user:
                        logger.warning(f"User {username} not found")
                        return False
                    if not checkpw(password.encode("utf-8"), user["password"].encode("utf-8")):
                        logger.warning(f"Password verification failed for {username}")
                        return False
                    cursor.execute(delete_user, (username, email))
                    connection.commit()
                    session.clear()
                    return True
            except Exception as e:
                logger.error(f"Error deleting user: {e}")
                return False
            finally:
                if connection:
                    release_connection(connection)
    except Exception as e:
        logger.error(f"Error deleting user: {e}")
        return False

def update_email_to_api(username, new_email, password):
    connection = None
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(check_user_exists_by_username, (username,))
                user = cursor.fetchone()
                if not user:
                    logger.warning(f"User {username} not found")
                    return False
                if not checkpw(password.encode("utf-8"), user["password"].encode("utf-8")):
                    logger.warning(f"Password verification failed for {username}")
                    return False
                cursor.execute(update_user_email, (new_email, username))
                connection.commit()
                return True
    except Exception as e:
        logger.error(f"Error updating email: {e}")
        return False