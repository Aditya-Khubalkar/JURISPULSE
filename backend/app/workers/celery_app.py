from celery import Celery
celery_app = Celery("jurispulse", broker="redis://localhost:6379/0")
