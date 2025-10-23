from db import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

class Todos(Base):
    __tablename__ = 'todos'
    id = Column(Integer, primary_key=True,index=True)
    name = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean,default=False)

