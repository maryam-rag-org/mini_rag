from pydantic import BaseModel

from .minirag_base import SQLAlchemyBase
from sqlalchemy import Column, Integer, DateTime, String ,func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy import Index

import uuid

class DataChunk(SQLAlchemyBase):
    
    #1- table name

    __tablename__ = "chunks"

    #2- table's columns
    chunk_id = Column(Integer, primary_key=True, autoincrement=True) # for indexing and joining the tables
    chunk_uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)  # for user and security 

    chunk_text = Column(String, nullable=False)
    chunk_metadata = Column(JSONB, nullable=True)
    chunk_order = Column(Integer, nullable=False)


    # Foreign Keys
    chunk_project_id = Column(Integer, ForeignKey("projects.project_id"), nullable=False)
    chunk_asset_id = Column(Integer, ForeignKey("assets.asset_id"), nullable=False)

    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
 

    # relationship between chunks and project
    project = relationship("Project", back_populates="chunks")

    # relationship between chunks and asset
    asset = relationship("Asset", back_populates="chunks")


    # Indexing
    __table_args__ = (
        Index('ix_chunk_project_id', chunk_project_id),
        Index('ix_chunk_asset_id', chunk_asset_id)
    )

class RetrievedDocument(BaseModel):
    text: str
    score: float
    
