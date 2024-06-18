from datetime import datetime

from sqlalchemy import Column, String, BigInteger
from sqlalchemy.dialects.postgresql import TIMESTAMP

from src.database import Base


class User(Base):
    """User model"""
    __tablename__ = 'user'

    id = Column(BigInteger, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    register_at = Column(TIMESTAMP, default=datetime.now)
    last_login = Column(TIMESTAMP, default=None)
