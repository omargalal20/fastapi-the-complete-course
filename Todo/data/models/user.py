import enum

from sqlalchemy import Column, Integer, String, Boolean, Enum

from data.database.postgres import Base


class Role(enum.Enum):
    ADMIN = "ADMIN"
    USER = "USER"

class User(Base):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(Enum(Role))
