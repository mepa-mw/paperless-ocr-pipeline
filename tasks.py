from background_worker import app
from parser_ocr import extract_text_smart
from models.main.document_text import SessionLocal, DocumentText
from models.paperless.documents_document import SessionPaperless, DocumentsDocument
from logger import logger
import datetime

@app.task(bind=True, rate_limit='1/s')
def process_document(self, paperless_doc_id, file_path, filename, original_filename):
    session = SessionLocal()
    # create or fetch record
    documentText = DocumentText(
        paperless_doc_id=paperless_doc_id,
        filename=filename,
        original_filename=original_filename,
        status='processing',
        source='upload'
    )
    session.add(documentText)
    session.commit()
    
    try:
        text, source = extract_text_smart(file_path)
        documentText.raw_text = text
        documentText.source = source
        documentText.status = 'done'
        documentText.processed_at = datetime.datetime.utcnow()
        session.commit()
        logger.info(f"Processed {filename} ({source})")
        
        update_paperless_ocr_content(paperless_doc_id, text)
    except Exception as e:
        logger.error(f"Error processing {filename}: {e}")
        documentText.status = 'error'
        session.commit()
    finally:
        session.close()
        SessionLocal.remove()
        
def update_paperless_ocr_content(document_id, text):
    session = SessionPaperless()
    try:
        document = session.query(DocumentsDocument).filter_by(id=document_id).first()
        if document:
            document.content = text
            document.modified = datetime.datetime.utcnow()
            session.commit()
            logger.info(f"Updated Paperless content for doc ID {document_id}")
        else:
            logger.warning(f"Paperless document with ID {document_id} not found")
    except Exception as e:
        logger.error(f"Failed to update Paperless document ID {document_id}: {e}")
    finally:
        session.close()