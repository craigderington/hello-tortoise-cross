from __future__ import absolute_import
import os
from celery import Celery
from celery.schedules import crontab
from .tasks import get_message, get_locations, log
from .config import config

# set up the celery app
app = Celery(__name__, 
             broker_url="0.0.0.0:5672/", 
             result_backend="rpc://",
             include=["stalks.tasks"])

# update the celery app config
app.config_from_object(config["development"])

# setup the periodic tasks
@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(60.0, get_locations, name="Get Network Locations")
    sender.add_periodic_task(30.0, get_message, name="Get Message Every 30 seconds.")


# debug task
@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))