"""
    This module defines models for api call and database
"""
from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Employee(Base):
    """
    Employee tables
    """
    __tablename__ = "employee"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    department = Column(String)


class EmployeeData(BaseModel):
    """
    Employee standard api call
    """
    first_name: str
    middle_name: Optional[str]
    last_name: str
    department: str
