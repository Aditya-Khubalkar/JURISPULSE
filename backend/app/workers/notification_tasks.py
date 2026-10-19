from .celery_app import celery_app
@celery_app.task
def send_reminder(hid: str): return True
