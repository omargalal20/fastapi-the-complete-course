from sqlalchemy import Column, Integer, String, Boolean

from data.database.sqlite import Base


class Todo(Base):
    __tablename__ = 'Todo'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
