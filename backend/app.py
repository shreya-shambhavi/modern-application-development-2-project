from flask import Flask
from flask_cors import CORS
from application.extensions import db, security, cache
from application.datastore import user_datastore
from application.create_initial_data import create_data
from application.views import create_views
from application.resources import *
from application.worker import celery_init_app
import flask_excel as excel
from celery.schedules import crontab
from application.tasks import daily_reminder, monthly_report

app = None

def create_app():
    app = Flask(__name__)
    app.debug = True
    CORS(app, resources = {r"/*": {"origins": "http://localhost:8080"}})

    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///iescpdata.sqlite3"
    app.config['SECRET_KEY'] = "secret-key"
    app.config['SECURITY_PASSWORD_SALT'] = "salty-password"

    app.config['SECURITY_TOKEN_AUTHENTICATION_HEADER'] = "Authentication-Token"
    # app.config['SECURITY_TOKEN_MAX_AGE'] = 3600 #1hr
    app.config['SECURITY_LOGIN_WITHOUT_CONFIRMATION'] = True

    app.config['CACHE_TYPE'] = "RedisCache"
    app.config['CACHE_REDIS_HOST'] = "localhost"
    app.config['CACHE_REDIS_PORT'] = 6379
    app.config['CACHE_REDIS_DB'] = 0
    app.config['CACHE_REDIS_URL'] = "redis://localhost:6379/0"
    # app.config['CACHE_DEFAULT_TIMEOUT'] = 300 #5min

    db.init_app(app)

    with app.app_context():
        
        security.init_app(app, user_datastore)

        db.create_all()

        create_data(user_datastore)

    app.config["WTF_CSRF_CHECK_DEFAULT"] = False
    app.config['SECURITY_CSRF_PROTECT_MECHANISMS'] = []
    app.config['SECURITY_CSRF_IGNORE_UNAUTH_ENDPOINTS'] = True
    
    create_views(app, user_datastore)
    api.init_app(app)

    return app

app = create_app()
celery_app = celery_init_app(app)
excel.init_excel(app)
cache.init_app(app)

@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(hour = 18, minute = 0), daily_reminder.s(), name = "Daily Reminder")
    sender.add_periodic_task(crontab(hour = 8, minute = 0, day_of_month = 1), monthly_report.s(), name = "Monthly Report")

if __name__ == '__main__':
    app.run()