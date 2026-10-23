#!/bin/sh
exec celery -A backend.app.workers.celery_app worker
