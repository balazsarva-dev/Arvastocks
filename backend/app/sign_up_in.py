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
from flask_mail import Message
from bcrypt import hashpw, checkpw, gensalt
import os
from celery_app import celery

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

@celery.task
def send_async_email(msg_data):
    from app import mail
    from flask_mail import Message
    
    try:
        msg = Message(
            subject=msg_data["subject"],
            sender=msg_data["sender"],
            recipients=msg_data["recipients"],
            body=msg_data["body"],
        )
        mail.send(msg)
        logger.info("Email sent successfully")
    except Exception as e:
        logger.error(f"Error sending email: {e}")


def send_contact_email(name, email, message):
    try:
        msg_data = {
            "subject": "Contact Form Submission",
            "sender": os.getenv("MAIL_DEFAULT_SENDER"),
            "recipients": [os.getenv("MAIL_DEFAULT_SENDER")],
            "body": f"Name: {name}\nEmail: {email}\nMessage: {message}",
        }
        send_async_email.delay(msg_data)
        return True
    except Exception as e:
        logger.error(f"Error sending message: {e}")
        return False

def registration_accepted_message(username, email):
    try:
        msg_data = {
            "subject": "Registration Accepted",
            "sender": os.getenv("MAIL_DEFAULT_SENDER"),
            "recipients": [email],
            "body": f"Hello {username},\n\nYour registration has been accepted.\n\nBest regards,\nThe Team",
        }
        send_async_email.delay(msg_data)
        return True
    except Exception as e:
        logger.error(f"Error sending registration message: {e}")
        return False


def update_password(username, old_password, new_password):
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
                    new_password = hashpw(new_password.encode("utf-8"), gensalt()).decode("utf-8")
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


def delete_user_from_db(username, email, password):
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

def update_email(username, new_email, password):
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