from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .jobscheduler import schedule_api

def start():
	scheduler = BackgroundScheduler()
	scheduler.add_job(schedule_api, 'interval', seconds=5)
	scheduler.start()