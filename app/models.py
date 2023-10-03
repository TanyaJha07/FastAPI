from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.expression import text
from .database import Base 

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=False)
    tittle = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, default=True)