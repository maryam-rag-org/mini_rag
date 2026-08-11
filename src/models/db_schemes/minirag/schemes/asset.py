from .minirag_base import SQLAlchemyBase
from sqlalchemy import Column, Integer, DateTime, String ,func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy import Index

import uuid

class Asset(SQLAlchemyBase):
    
    #1- table name

    __tablename__ = "assets"

    #2- table's columns
    asset_id = Column(Integer, primary_key=True, autoincrement=True) # for indexing and joining the tables
    asset_uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)  # for user and security 

    asset_type = Column(String, nullable=False)
    asset_name = Column(String, nullable=False)
    asset_size = Column(Integer, nullable=False)
    asset_config = Column(JSONB, nullable=True)

    
    # Foreign Keys
    asset_project_id = Column(Integer, ForeignKey("projects.project_id"), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    # relationship between asset and project
    project = relationship("Project", back_populates="assets")
    chunks = relationship("DataChunk", back_populates="asset")

    # Indexing
    __table_args__ = (
        Index('ix_asset_project_id', asset_project_id),
        Index('ix_asset_type', asset_type)
    )
    
    
