from app.settings import logger
from flask import Flask
from flask_compress import Compress
from flask_caching import Cache
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
import pymysql
from dbutils.pooled_db import PooledDB
from app.configs import Config
from flask_cors import CORS
from celery_app import make_celery

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["https://arvastocks.com", "https://www.arvastocks.com", "http://localhost:5173"]}}, supports_credentials=True)

app.config.from_object(Config)

def create_db_pool():
    try:
        db_pool = PooledDB(
            creator=pymysql,
            host=app.config["DB_HOST"],
            user=app.config["MARIADB_USER"],
            password=app.config["MARIADB_PASSWORD"],
            db=app.config["MARIADB_DATABASE"],
            port=app.config["DB_PORT"],
            cursorclass=pymysql.cursors.DictCursor,
        )
        logger.info("Database pool created successfully.")
        return db_pool
    except pymysql.MySQLError as e:
        logger.error(f"Error creating database pool: {e}")
        raise
    except Exception as e:
        logger.error(f"Error creating database pool: {e}")
        raise

def register_extensions(app):
    cache = Cache(app)
    compress = Compress(app)
    mail = Mail(app)
    csrf = CSRFProtect(app)
    celery = make_celery(app)
    logger.info("Extensions registered successfully.")
    return cache, compress, mail, csrf, celery


from app.db import init_db

def init_app(app):
    try:
        with app.app_context():
            init_db(app)
            logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing the database: {type(e).__name__}: {e}")
        raise


app.db_pool = create_db_pool()

init_app(app)

cache, compress, mail, csrf, celery = register_extensions(app)
from app.api_routes import api as api_blueprint
csrf.exempt(api_blueprint)
app.register_blueprint(api_blueprint, url_prefix="/api")

logger.info("Application started")
