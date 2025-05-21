import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import DATABASE_PAPERLESS_URL


engine = create_engine(DATABASE_PAPERLESS_URL)
SessionPaperless = sessionmaker(bind=engine)
Base = declarative_base()

class DocumentsDocument(Base):
    __tablename__ = "documents_document"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True)
    title = Column(String(128), nullable=False)
    content = Column(Text, nullable=False)
    created = Column(TIMESTAMP(timezone=True), nullable=False)
    modified = Column(TIMESTAMP(timezone=True), nullable=False)
    correspondent_id = Column(Integer, nullable=True)
    checksum = Column(String(32), nullable=False)
    added = Column(TIMESTAMP(timezone=True), nullable=False)
    storage_type = Column(String(11), nullable=False)
    filename = Column(String(1024), nullable=True)
    archive_serial_number = Column(Integer, nullable=True)
    document_type_id = Column(Integer, nullable=True)
    mime_type = Column(String(256), nullable=False)
    archive_checksum = Column(String(32), nullable=True)
    archive_filename = Column(String(1024), nullable=True)
    storage_path_id = Column(Integer, nullable=True)
    original_filename = Column(String(1024), nullable=True)
    owner_id = Column(Integer, nullable=True)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    restored_at = Column(TIMESTAMP(timezone=True), nullable=True)
    transaction_id = Column(UUID(as_uuid=True), nullable=True)
    page_count = Column(Integer, nullable=True)
    
    @classmethod
    def get_by_filename(cls, session, filename):
        """
        Retrieve the first document matching the given filename.
        """
        return session.query(cls).filter(cls.filename == filename).first()