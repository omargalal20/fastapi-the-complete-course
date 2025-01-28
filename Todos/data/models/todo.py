from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

from data.database.postgres import Base


class Todo(Base):
    __tablename__ = 'Todo'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("User.id"))
