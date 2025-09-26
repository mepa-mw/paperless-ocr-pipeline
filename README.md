
# PAPERLESS-NGX OCR PIPELINE

## Setup Instructions

### 1. Clone the repository
```
git clone https://github.com/mepa-mw/paperless-ocr-pipeline.git
cd paperless-ocr-pipeline
```

### 2. Create and activate a Python virtual environment
```
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```
pip install -r requirements.txt
```

### 4. Configure environment variables
Copy `.env.example` to `.env` and update values as needed (see sample below):
```
cp example.env .env
# Edit .env with your database, directories, and other settings
```

Key variables in `.env`:
- Database settings (`DB_HOST`, `DB_NAME`, etc.)
- Directories (`MEDIA_DIR`, `LOGS_DIR`, etc.)
- Worker and watcher configs (`WORKER_BROKER`, `WATCHER_CHECK_INTERVAL`, etc.)

### 5. Start the watcher (document monitor)
You can run the watcher manually:
```
source venv/bin/activate
python watcher.py
```
Or set it up as a systemd service (recommended for production):

#### Using systemd services (recommended for production)

Systemd service files for watcher and celery worker are provided in the `scripts` directory:
- `scripts/paperless-ocr-watcher.service`
- `scripts/paperless-ocr-celery.service`

To install and enable these services:
1. Copy the service files to `/etc/systemd/system/`:
	```
	sudo cp scripts/paperless-ocr-watcher.service /etc/systemd/system/
	sudo cp scripts/paperless-ocr-celery.service /etc/systemd/system/
	```
2. Edit the service files if needed (e.g., set `User=mepa` in watcher service).
3. Reload systemd to recognize new services:
	```
	sudo systemctl daemon-reload
	```
4. Enable the services to start on boot:
	```
	sudo systemctl enable paperless-ocr-watcher
	sudo systemctl enable paperless-ocr-celery
	```
5. Start the services:
	```
	sudo systemctl start paperless-ocr-watcher
	sudo systemctl start paperless-ocr-celery
	```
6. Check status and logs:
	```
	sudo systemctl status paperless-ocr-watcher
	sudo systemctl status paperless-ocr-celery
	journalctl -u paperless-ocr-watcher -f
	journalctl -u paperless-ocr-celery -f
	```

---

### 6. Start the Celery worker
Run manually:
```
source venv/bin/activate
celery -A background_worker.app worker --loglevel=info --concurrency=1
```
Or set it up as a systemd service:
See `scripts/paperless-ocr-celery.service` for a sample service file.

---

## Notes
- Ensure your `.env` is correctly configured before starting services.
- Both watcher and celery worker should be running for the pipeline to function.
- For production, use systemd to keep services running and restart on failure.

