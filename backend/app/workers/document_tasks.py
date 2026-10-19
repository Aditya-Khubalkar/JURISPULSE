from .celery_app import celery_app
@celery_app.task
def process_doc(doc_id: str): return {"doc_id": doc_id, "ocr": "completed"}
