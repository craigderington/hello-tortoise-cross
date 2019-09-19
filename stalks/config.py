import os
from kombu import Queue, Exchange

BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    SECRET_KEY = os.urandom(32)
    CELERY_TIMEZONE = "America/New_York"
    CELERY_ENABLE_UTC = True
    TASK_SERIALIZER = "json"
    RESULT_SERIALZIER = "json"
    CELERY_ACCEPT_CONTENT = ["json", "yaml"]    

    # define the tasks queues
    CELERY_QUEUES = (
        Queue("messages", Exchange("default"), routing_key="api.messages"),
        Queue("locations", Exchange("default"), routing_key="api.locations"),
        Queue("devices", Exchange("default"), routing_key="api.devices"),
    )

    # define the task routes
    CELERY_ROUTES = {
        "messages": {"queue": "messages", "routing_key": "api.messages"},
        "locations": {"queue": "locations", "routing_key": "api.locations"},
        "devices": {"queue": "devices", "routing_key": "api.devices"}
    }

    # authentication for rest api
    BF_USERNAME = os.environ.get("BF_USER")
    BF_PASSWORD = os.environ.get("BF_PWD")

    # base url
    SNOW_BASE_URL = "https://championsolutionsgroupdemo2.service-now.com/api/x_328385_restapi/bbi/"
    API_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE"]


class DevelopmentConfig(Config):
    DEBUG = True
    PORT = 5880
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "sqlite:////bettlejuice.db"
    
    CELERY_BROKER_URL = "pyamqp://0.0.0.0:5672/"
    CELERY_RESULT_BACKEND = "redis://0.0.0.0:6379/0"
    
    MONGO_SERVER = "0.0.0.0:27017"
    MONGO_DB = "netauto"


class DockerConfig(Config):
    DEBUG = True
    PORT = 5555
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "sqlite:////bettlejuice.db"
    
    CELERY_BROKER_URL = "pyamqp://172.17.0.2:5672/"
    CELERY_RESULT_BACKEND = "redis://172.17.0.3:6379/0"
    
    MONGO_SERVER = "172.17.0.5:27017"
    MONGO_DB = "netauto"


class DockerComposeConfig(Config):
    DEBUG = True
    PORT = 5555
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:yufakay3!@mysql:3306/netauto"
    SQLALCHEMY_DATABASE_URI = "sqlite:////bettlejuice.db"

    CELERY_TIMEZONE = "US/Eastern"
    CELERY_BROKER_URL = "pyamqp://rabbitmq:5672/"
    CELERY_RESULT_BACKEND = "redis://redis:6379/0"
    
    MONGO_SERVER = "database:27017"
    MONGO_DB = "netauto"


class ProductionConfig(Config):
    DEBUG = False


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "docker": DockerConfig,
    "docker-compose": DockerComposeConfig
}