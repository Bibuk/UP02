from sqlalchemy import create_engine, Column, Integer, String, Text, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime, timezone
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

DATABASE_URL = "sqlite:///./job_catalog.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Vacancy(Base):
    """Модель вакансии"""
    __tablename__ = "vacancies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    company = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=False)
    salary_min = Column(Float, nullable=True)
    salary_max = Column(Float, nullable=True)
    location = Column(String, index=True, nullable=False)
    employment_type = Column(String, nullable=False)  # полная/частичная/удаленная
    experience = Column(String, nullable=False)  # без опыта/1-3 года/3-6 лет/более 6 лет
    skills = Column(String, nullable=True)  # через запятую
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class Resume(Base):
    """Модель резюме"""
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True, nullable=False)
    position = Column(String, index=True, nullable=False)
    about = Column(Text, nullable=False)
    salary_expectation = Column(Float, nullable=True)
    location = Column(String, index=True, nullable=False)
    employment_type = Column(String, nullable=False)  # полная/частичная/удаленная
    experience_years = Column(String, nullable=False)  # без опыта/1-3 года/3-6 лет/более 6 лет
    skills = Column(String, nullable=True)  # через запятую
    education = Column(String, nullable=True)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


def get_db():
    """Dependency для получения сессии БД"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Создание таблиц в БД"""
    Base.metadata.create_all(bind=engine)
