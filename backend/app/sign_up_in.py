from app.queries import (
    check_user_exists,
    check_user_exists_by_username,
    insert_user,
    delete_user,
    update_user_password,
    update_user_email,
)
from app import app
from app.db import get_connection, release_connection
from app.settings import logger
from bcrypt import hashpw, checkpw, gensalt
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

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


def send_email_via_sendgrid(subject, body, from_email, to_email):
    message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        plain_text_content=body
    )
    try:
        sg = SendGridAPIClient(app.config["SENDGRID_API_KEY"])
        response = sg.send(message)
        logger.info(f"Email sent to {to_email} with status code {response.status_code}")
        return True
    except Exception as e:
        logger.error(f"Error sending email: {e}", exc_info=True)
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