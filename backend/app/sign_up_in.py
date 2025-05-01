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
from email.message import EmailMessage
from aiosmtplib import send
import asyncio

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


async def send_email(subject, body, from_email, to_email):
    try:
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = from_email
        msg["To"] = to_email
        msg.set_content(body)

        smtp_host = app.config["MAIL_SERVER"]
        smtp_port = app.config["MAIL_PORT"]
        smtp_username = app.config["MAIL_USERNAME"]
        smtp_password = app.config["MAIL_PASSWORD"]
        
        await send(
            msg,
            hostname=smtp_host,
            port=smtp_port,
            username=smtp_username,
            password=smtp_password,
            use_tls=False,
            start_tls=True
        )
        return True
    except Exception as e:
        logger.error(f"Error sending email: {e}", exc_info=True)
        return False

def send_email_in_background(subject, body, from_email, to_email):
    try:
        asyncio.run(send_email(subject, body, from_email, to_email))
    except Exception as e:
        logger.error(f"Error sending email in background: {e}", exc_info=True)

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