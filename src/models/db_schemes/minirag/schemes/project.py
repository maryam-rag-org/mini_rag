from .minirag_base import SQLAlchemyBase
from sqlalchemy import Column, Integer, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

import uuid

class Project(SQLAlchemyBase):
    
    #1- table name

    __tablename__ = "projects"

    #2- table's columns
    project_id = Column(Integer, primary_key=True, autoincrement=True) # for indexing and joining the tables
    project_uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)  # for user and security 

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    # relationships
    chunks = relationship("DataChunk", back_populates="project")
    assets = relationship("Asset", back_populates="project")