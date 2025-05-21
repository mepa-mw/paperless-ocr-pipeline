import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

PGPASS_FILE = os.path.expanduser("~/.pgpass")

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", 5432)
DB_NAME = os.getenv("DB_NAME", "paperless_ocr_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "")

DB_PAPERLESS_HOST = os.getenv("DB_PAPERLESS_HOST", "localhost")
DB_PAPERLESS_PORT = os.getenv("DB_PAPERLESS_PORT", 5432)
DB_PAPERLESS_NAME = os.getenv("DB_PAPERLESS_NAME", "paperless_db")
DB_PAPERLESS_USER = os.getenv("DB_PAPERLESS_USER", "postgres")
DB_PAPERLESS_PASS = os.getenv("DB_PAPERLESS_PASS", "")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}?sslmode=disable"
DATABASE_PAPERLESS_URL = f"postgresql://{DB_PAPERLESS_USER}:{DB_PAPERLESS_PASS}@{DB_PAPERLESS_HOST}:{DB_PAPERLESS_PORT}/{DB_PAPERLESS_NAME}?sslmode=disable"

WATCHER_CHECK_INTERVAL = os.getenv("WATCHER_CHECK_INTERVAL", 300)

WORKER_NAME = os.getenv("WORKER_NAME", "")
WORKER_BROKER = os.getenv("WORKER_BROKER", "")
WORKER_BACKEND = os.getenv("WORKER_BACKEND", "")

BACKUP_DIR = os.getenv("BACKUP_DIR", "")
MEDIA_DIR = os.getenv("MEDIA_DIR", "")
LOGS_DIR = os.getenv("LOGS_DIR", "")

MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "")
MINIO_BUCKET = os.getenv("MINIO_BUCKET", "paperless-backups")