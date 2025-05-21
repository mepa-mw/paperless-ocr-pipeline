import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from config import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()

class DocumentText(Base):
    __tablename__ = 'document_texts'
    id = Column(Integer, primary_key=True, index=True)
    paperless_doc_id = Column(Integer)
    original_filename = Column(String)
    filename = Column(String, nullable=False)
    raw_text = Column(Text)
    source = Column(String, nullable=False)  # 'upload', 'parsed', or 'ocr'
    status = Column(String, default='pending')  # pending, processing, done, error
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    processed_at = Column(DateTime)

# create tables
Base.metadata.create_all(bind=engine)