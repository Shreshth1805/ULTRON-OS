from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from app.schemas import NodeCreate, NodeUpdate
from typing import Optional

class Node(Base):
    __tablename__ = "nodes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    type = Column(String, index=True)
    description = Column(String, index=True)
    workflow_id = Column(Integer, ForeignKey("workflows.id"))
    workflow = relationship("Workflow", back_populates="nodes")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    def __init__(self, name: str, type: str, description: str, workflow_id: int):
        self.name = name
        self.type = type
        self.description = description
        self.workflow_id = workflow_id

    @classmethod
    def get_node(cls, db, node_id: int):
        return db.query(cls).filter(cls.id == node_id).first()

    @classmethod
    def get_nodes(cls, db, workflow_id: int):
        return db.query(cls).filter(cls.workflow_id == workflow_id).all()

    @classmethod
    def create_node(cls, db, node: NodeCreate):
        db_node = cls(name=node.name, type=node.type, description=node.description, workflow_id=node.workflow_id)
        db.add(db_node)
        db.commit()
        db.refresh(db_node)
        return db_node

    @classmethod
    def update_node(cls, db, node_id: int, node: NodeUpdate):
        db_node = cls.get_node(db, node_id)
        if db_node:
            db_node.name = node.name
            db_node.type = node.type
            db_node.description = node.description
            db.commit()
            db.refresh(db_node)
            return db_node
        return None

    @classmethod
    def delete_node(cls, db, node_id: int):
        db_node = cls.get_node(db, node_id)
        if db_node:
            db.delete(db_node)
            db.commit()
            return True
        return False