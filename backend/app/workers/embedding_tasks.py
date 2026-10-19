from .celery_app import celery_app
@celery_app.task
def embed_case(cid: str): return {"cid": cid}
