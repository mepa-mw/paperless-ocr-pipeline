# PAPERLESS-NGX OCR PIPELINE

- In a scenerio where celery is interacting with the database, as it stands, it's best to have concurrency set to 1:
- `celery -A background_worker.app worker --loglevel=info --concurrency=1`

