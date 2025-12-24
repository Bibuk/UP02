from fastapi import FastAPI, Depends, HTTPException, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List, Optional
import database
import schemas
from database import get_db, init_db

app = FastAPI(
    title="Каталог вакансий и резюме",
    description="API для управления вакансиями и резюме с поиском и фильтрацией",
    version="1.0.0"
)

init_db()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")



@app.post("/api/vacancies/", response_model=schemas.VacancyResponse, status_code=201)
def create_vacancy(vacancy: schemas.VacancyCreate, db: Session = Depends(get_db)):
    db_vacancy = database.Vacancy(**vacancy.model_dump())
    db.add(db_vacancy)
    db.commit()
    db.refresh(db_vacancy)
    return db_vacancy


@app.get("/api/vacancies/", response_model=List[schemas.VacancyResponse])
def get_vacancies(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    vacancies = db.query(database.Vacancy).offset(skip).limit(limit).all()
    return vacancies


@app.get("/api/vacancies/{vacancy_id}", response_model=schemas.VacancyResponse)
def get_vacancy(vacancy_id: int, db: Session = Depends(get_db)):
    vacancy = db.query(database.Vacancy).filter(database.Vacancy.id == vacancy_id).first()
    if not vacancy:
        raise HTTPException(status_code=404, detail="Вакансия не найдена")
    return vacancy


@app.put("/api/vacancies/{vacancy_id}", response_model=schemas.VacancyResponse)
def update_vacancy(
    vacancy_id: int,
    vacancy_update: schemas.VacancyUpdate,
    db: Session = Depends(get_db)
):
    vacancy = db.query(database.Vacancy).filter(database.Vacancy.id == vacancy_id).first()
    if not vacancy:
        raise HTTPException(status_code=404, detail="Вакансия не найдена")
    
    update_data = vacancy_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(vacancy, field, value)
    
    db.commit()
    db.refresh(vacancy)
    return vacancy


@app.delete("/api/vacancies/{vacancy_id}", status_code=204)
def delete_vacancy(vacancy_id: int, db: Session = Depends(get_db)):
    vacancy = db.query(database.Vacancy).filter(database.Vacancy.id == vacancy_id).first()
    if not vacancy:
        raise HTTPException(status_code=404, detail="Вакансия не найдена")
    
    db.delete(vacancy)
    db.commit()
    return None


@app.get("/api/vacancies/search/", response_model=List[schemas.VacancyResponse])
def search_vacancies(
    query: Optional[str] = Query(None, description="Поиск по названию, компании или навыкам"),
    location: Optional[str] = Query(None, description="Фильтр по местоположению"),
    employment_type: Optional[str] = Query(None, description="Фильтр по типу занятости"),
    experience: Optional[str] = Query(None, description="Фильтр по опыту"),
    salary_min: Optional[float] = Query(None, description="Минимальная зарплата"),
    salary_max: Optional[float] = Query(None, description="Максимальная зарплата"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    vacancies_query = db.query(database.Vacancy)
    
    if query:
        search_filter = (
            database.Vacancy.title.contains(query) |
            database.Vacancy.company.contains(query) |
            database.Vacancy.skills.contains(query) |
            database.Vacancy.description.contains(query)
        )
        vacancies_query = vacancies_query.filter(search_filter)
    
    if location:
        vacancies_query = vacancies_query.filter(database.Vacancy.location.contains(location))
    
    if employment_type:
        vacancies_query = vacancies_query.filter(database.Vacancy.employment_type == employment_type)
    
    if experience:
        vacancies_query = vacancies_query.filter(database.Vacancy.experience == experience)
    
    if salary_min is not None:
        vacancies_query = vacancies_query.filter(database.Vacancy.salary_max >= salary_min)
    
    if salary_max is not None:
        vacancies_query = vacancies_query.filter(database.Vacancy.salary_min <= salary_max)
    
    vacancies = vacancies_query.offset(skip).limit(limit).all()
    return vacancies


@app.post("/api/resumes/", response_model=schemas.ResumeResponse, status_code=201)
def create_resume(resume: schemas.ResumeCreate, db: Session = Depends(get_db)):
    db_resume = database.Resume(**resume.model_dump())
    db.add(db_resume)
    db.commit()
    db.refresh(db_resume)
    return db_resume


@app.get("/api/resumes/", response_model=List[schemas.ResumeResponse])
def get_resumes(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    resumes = db.query(database.Resume).offset(skip).limit(limit).all()
    return resumes


@app.get("/api/resumes/{resume_id}", response_model=schemas.ResumeResponse)
def get_resume(resume_id: int, db: Session = Depends(get_db)):
    resume = db.query(database.Resume).filter(database.Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Резюме не найдено")
    return resume


@app.put("/api/resumes/{resume_id}", response_model=schemas.ResumeResponse)
def update_resume(
    resume_id: int,
    resume_update: schemas.ResumeUpdate,
    db: Session = Depends(get_db)
):
    resume = db.query(database.Resume).filter(database.Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Резюме не найдено")
    
    update_data = resume_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(resume, field, value)
    
    db.commit()
    db.refresh(resume)
    return resume


@app.delete("/api/resumes/{resume_id}", status_code=204)
def delete_resume(resume_id: int, db: Session = Depends(get_db)):
    resume = db.query(database.Resume).filter(database.Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Резюме не найдено")
    
    db.delete(resume)
    db.commit()
    return None


@app.get("/api/resumes/search/", response_model=List[schemas.ResumeResponse])
def search_resumes(
    query: Optional[str] = Query(None, description="Поиск по должности, ФИО или навыкам"),
    location: Optional[str] = Query(None, description="Фильтр по местоположению"),
    employment_type: Optional[str] = Query(None, description="Фильтр по типу занятости"),
    experience_years: Optional[str] = Query(None, description="Фильтр по опыту"),
    salary_min: Optional[float] = Query(None, description="Минимальная зарплата"),
    salary_max: Optional[float] = Query(None, description="Максимальная зарплата"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    resumes_query = db.query(database.Resume)
    
    if query:
        search_filter = (
            database.Resume.position.contains(query) |
            database.Resume.full_name.contains(query) |
            database.Resume.skills.contains(query) |
            database.Resume.about.contains(query)
        )
        resumes_query = resumes_query.filter(search_filter)
    
    if location:
        resumes_query = resumes_query.filter(database.Resume.location.contains(location))
    
    if employment_type:
        resumes_query = resumes_query.filter(database.Resume.employment_type == employment_type)
    
    if experience_years:
        resumes_query = resumes_query.filter(database.Resume.experience_years == experience_years)
    
    if salary_min is not None:
        resumes_query = resumes_query.filter(database.Resume.salary_expectation >= salary_min)
    
    if salary_max is not None:
        resumes_query = resumes_query.filter(database.Resume.salary_expectation <= salary_max)
    
    resumes = resumes_query.offset(skip).limit(limit).all()
    return resumes


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/vacancies", response_class=HTMLResponse)
def vacancies_page(request: Request):
    return templates.TemplateResponse("vacancies.html", {"request": request})


@app.get("/resumes", response_class=HTMLResponse)
def resumes_page(request: Request):
    return templates.TemplateResponse("resumes.html", {"request": request})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
