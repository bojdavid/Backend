from .database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, TIMESTAMP, func
from sqlalchemy.sql import expression
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__ = "posts_2"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(String(255), nullable=False)
    rating  = Column(Integer, nullable=False)
    published = Column(Boolean, nullable=False, server_default=expression.true())
    created_at = Column(TIMESTAMP(timezone=True), nullable=False , server_default=func.current_timestamp())
    owner_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False) 
    owner = relationship("User")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False , server_default=func.current_timestamp())

class Votes(Base):
    __tablename__ = "votes"

    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False, primary_key=True) 
    post_id = Column(Integer, ForeignKey('posts_2.id', ondelete="CASCADE"), nullable=False, primary_key=True) 