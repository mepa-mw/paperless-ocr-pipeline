import logging
import sys
from datetime import date
from celery import Celery, signals
from config import WORKER_NAME, WORKER_BROKER, WORKER_BACKEND, LOGS_DIR

# Initialize Celery app
app = Celery(
    main=WORKER_NAME,
    broker=WORKER_BROKER,
    backend=WORKER_BACKEND,
    include=['tasks']
)

# Prevent Celery from hijacking the root logger
app.conf.worker_hijack_root_logger = False

# Define the logging setup function
@signals.setup_logging.connect
def setup_celery_logging(**kwargs):
    # Create formatter
    formatter = logging.Formatter(fmt="[%(asctime)s] %(name)s.%(levelname)s: %(message)s")

    # Create stream handler
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)

    # Create file handler
    log_file_date = date.today().strftime("%d_%m_%Y")
    celery_log_filename = f"{LOGS_DIR}/celery_{log_file_date}.log"
    file_handler = logging.FileHandler(filename=celery_log_filename)
    file_handler.setFormatter(formatter)

    # Get the 'celery' logger and configure it
    celery_logger = logging.getLogger('celery')
    celery_logger.setLevel(logging.INFO)
    celery_logger.handlers = [stream_handler, file_handler]
    celery_logger.propagate = False
