from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime


class VacancyBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Название вакансии")
    company: str = Field(..., min_length=1, max_length=200, description="Название компании")
    description: str = Field(..., min_length=10, description="Описание вакансии")
    salary_min: Optional[float] = Field(None, ge=0, description="Минимальная зарплата")
    salary_max: Optional[float] = Field(None, ge=0, description="Максимальная зарплата")
    location: str = Field(..., min_length=1, description="Местоположение")
    employment_type: str = Field(..., description="Тип занятости")
    experience: str = Field(..., description="Требуемый опыт")
    skills: Optional[str] = Field(None, description="Навыки (через запятую)")


class VacancyCreate(VacancyBase):
    pass


class VacancyUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    company: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=10)
    salary_min: Optional[float] = Field(None, ge=0)
    salary_max: Optional[float] = Field(None, ge=0)
    location: Optional[str] = None
    employment_type: Optional[str] = None
    experience: Optional[str] = None
    skills: Optional[str] = None


class VacancyResponse(VacancyBase):
    id: int
    created_at: datetime
    
    model_config = {"from_attributes": True}


class ResumeBase(BaseModel):
    full_name: str = Field(..., min_length=1, max_length=200, description="ФИО")
    position: str = Field(..., min_length=1, max_length=200, description="Желаемая должность")
    about: str = Field(..., min_length=10, description="О себе")
    salary_expectation: Optional[float] = Field(None, ge=0, description="Ожидаемая зарплата")
    location: str = Field(..., min_length=1, description="Местоположение")
    employment_type: str = Field(..., description="Желаемый тип занятости")
    experience_years: str = Field(..., description="Опыт работы")
    skills: Optional[str] = Field(None, description="Навыки (через запятую)")
    education: Optional[str] = Field(None, description="Образование")
    email: EmailStr = Field(..., description="Email")
    phone: Optional[str] = Field(None, description="Телефон")


class ResumeCreate(ResumeBase):
    pass


class ResumeUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=1, max_length=200)
    position: Optional[str] = Field(None, min_length=1, max_length=200)
    about: Optional[str] = Field(None, min_length=10)
    salary_expectation: Optional[float] = Field(None, ge=0)
    location: Optional[str] = None
    employment_type: Optional[str] = None
    experience_years: Optional[str] = None
    skills: Optional[str] = None
    education: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None


class ResumeResponse(ResumeBase):
    id: int
    created_at: datetime
    
    model_config = {"from_attributes": True}
