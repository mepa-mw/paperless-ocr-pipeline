import os
import time
from models.main.document_text import SessionLocal, DocumentText
from models.paperless.documents_document import SessionPaperless, DocumentsDocument
from tasks import process_document
from logger import logger
from config import MEDIA_DIR, WATCHER_CHECK_INTERVAL

def get_uploaded_files():
    """Scan media directory and list PDF files"""
    return [
        os.path.join(MEDIA_DIR, f)
        for f in os.listdir(MEDIA_DIR)
        if f.lower().endswith('.pdf')
    ]


def already_processed(session, filename):
    return session.query(DocumentText).filter_by(filename=filename).first() is not None

def get_paperless_document(session, filename):
    return DocumentsDocument.get_by_filename(session, filename)

def main():
    logger.info("Watcher started, scanning for new documents...")
    while True:
        try:
            files = get_uploaded_files()

            # Open sessions once per iteration
            local_session = SessionLocal()
            paperless_session = SessionPaperless()

            for file_path in files:
                filename = os.path.basename(file_path)
                if not already_processed(local_session, filename):
                    paperlessDocument = get_paperless_document(paperless_session, filename)
                    paperlessDocumentId = paperlessDocument.id if paperlessDocument else 0
                    paperlessOriginalFilename = paperlessDocument.original_filename if paperlessDocument else None
                    
                    logger.info(f"Enqueuing {filename} for processing")
                    process_document.delay(
                        paperless_doc_id=paperlessDocumentId,
                        file_path=file_path,
                        filename=filename,
                        original_filename=paperlessOriginalFilename
                    )

            local_session.close()
            paperless_session.close()
            SessionLocal.remove()  # important when using scoped_session

        except Exception as e:
            logger.error(f"Watcher error: {e}")

        time.sleep(int(WATCHER_CHECK_INTERVAL))


if __name__ == '__main__':
    main()