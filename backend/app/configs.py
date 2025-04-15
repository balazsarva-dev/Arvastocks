import os
from dotenv import load_dotenv
from app.settings import logger

# Load environment variables from .env file
# Make sure to create a .env file in the root directory of your project with the required variables.

load_dotenv()

# This function retrieves an environment variable and converts it to the specified type.
# If the variable is not found, it raises an error or returns a default value.

def get_env_variable(var_name, default=None, type=str):
    env_var = os.getenv(var_name)
    if env_var is None:
        if default is None:
            logger.error(f"Missing environment variable: {var_name}")
            raise ValueError(f"Missing environment variable: {var_name}")
        else:
            return default
    
    if type == bool:
        env_var = env_var.lower() == 'true'
        return env_var
    
    try:
        return type(env_var)
    except ValueError:
        logger.error(f"Invalid type for environment variable {var_name}. Expected {type.__name__}.")
        raise ValueError(f"Invalid type for environment variable {var_name}. Expected {type.__name__}.")

# This class contains the configuration settings for the application.
# It retrieves values from environment variables and provides default values where necessary.

class Config:
    DEBUG = get_env_variable("DEBUG", default=False, type=bool)
    TESTING = get_env_variable("TESTING", default=False, type=bool)
    SECRET_KEY = get_env_variable("SECRET_KEY")
    MAIL_SERVER = get_env_variable("MAIL_SERVER")
    MAIL_PORT = get_env_variable("MAIL_PORT", default=587, type=int)
    MAIL_USE_TLS = get_env_variable("MAIL_USE_TLS", default=True, type=bool)
    MAIL_USE_SSL = get_env_variable("MAIL_USE_SSL", default=False, type=bool)
    MAIL_USERNAME = get_env_variable("MAIL_USERNAME")
    MAIL_PASSWORD = get_env_variable("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = get_env_variable("MAIL_DEFAULT_SENDER")
    DB_HOST = get_env_variable("DB_HOST")
    MARIADB_USER = get_env_variable("MARIADB_USER")
    MARIADB_PASSWORD = get_env_variable("MARIADB_PASSWORD")
    MARIADB_DATABASE = get_env_variable("MARIADB_DATABASE")
    DB_PORT = get_env_variable("DB_PORT", default=3306, type=int)
    API_KEY = get_env_variable("API_KEY")
