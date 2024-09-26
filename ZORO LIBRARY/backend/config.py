class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///zorolibrary.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "sshitsasecret"
    CELERY_BROKER_URL = 'redis://127.0.0.1:6379/1'
    CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/2'
    MAIL_SERVER = 'localhost'
    MAIL_PORT = 1025
    CACHE_TYPE = 'redis'
    CACHE_REDIS_URL = 'redis://127.0.0.1:6379/3'
    # for mailhog 'localhost:8025/'
    # celery -A app.celery worker --loglevel=info
    # celery -A app.celery beat --max-interval 1 -l info
    # @cache.cached(timeout=10)