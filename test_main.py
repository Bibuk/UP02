import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function")
def client():
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    Base.metadata.drop_all(bind=engine)


def test_create_vacancy(client):
    vacancy_data = {
        "title": "Python Developer",
        "company": "Tech Company",
        "description": "Ищем опытного Python разработчика",
        "salary_min": 100000,
        "salary_max": 200000,
        "location": "Москва",
        "employment_type": "Полная",
        "experience": "3-6 лет",
        "skills": "Python, Django, PostgreSQL"
    }
    
    response = client.post("/api/vacancies/", json=vacancy_data)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == vacancy_data["title"]
    assert data["company"] == vacancy_data["company"]
    assert "id" in data


def test_get_vacancies(client):
    for i in range(3):
        client.post("/api/vacancies/", json={
            "title": f"Vacancy {i}",
            "company": f"Company {i}",
            "description": f"Description {i}",
            "location": "Москва",
            "employment_type": "Полная",
            "experience": "1-3 года"
        })
    
    response = client.get("/api/vacancies/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3


def test_get_vacancy_by_id(client):
    create_response = client.post("/api/vacancies/", json={
        "title": "Test Vacancy",
        "company": "Test Company",
        "description": "Test Description",
        "location": "Москва",
        "employment_type": "Полная",
        "experience": "1-3 года"
    })
    vacancy_id = create_response.json()["id"]
    
    response = client.get(f"/api/vacancies/{vacancy_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == vacancy_id
    assert data["title"] == "Test Vacancy"


def test_update_vacancy(client):
    create_response = client.post("/api/vacancies/", json={
        "title": "Old Title",
        "company": "Test Company",
        "description": "Test Description",
        "location": "Москва",
        "employment_type": "Полная",
        "experience": "1-3 года"
    })
    vacancy_id = create_response.json()["id"]
    
    update_data = {"title": "New Title"}
    response = client.put(f"/api/vacancies/{vacancy_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Title"


def test_delete_vacancy(client):
    create_response = client.post("/api/vacancies/", json={
        "title": "Test Vacancy",
        "company": "Test Company",
        "description": "Test Description",
        "location": "Москва",
        "employment_type": "Полная",
        "experience": "1-3 года"
    })
    vacancy_id = create_response.json()["id"]
    
    response = client.delete(f"/api/vacancies/{vacancy_id}")
    assert response.status_code == 204
    
    get_response = client.get(f"/api/vacancies/{vacancy_id}")
    assert get_response.status_code == 404


def test_search_vacancies(client):
    client.post("/api/vacancies/", json={
        "title": "Python Developer",
        "company": "Company A",
        "description": "Python job",
        "location": "Москва",
        "employment_type": "Полная",
        "experience": "1-3 года",
        "skills": "Python, Django"
    })
    
    client.post("/api/vacancies/", json={
        "title": "Java Developer",
        "company": "Company B",
        "description": "Java job",
        "location": "Санкт-Петербург",
        "employment_type": "Удаленная",
        "experience": "3-6 лет",
        "skills": "Java, Spring"
    })
    
    response = client.get("/api/vacancies/search/?query=Python")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert "Python" in data[0]["title"]
    
    response = client.get("/api/vacancies/search/?location=Санкт-Петербург")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["location"] == "Санкт-Петербург"


def test_create_resume(client):
    resume_data = {
        "full_name": "Иванов Иван Иванович",
        "position": "Python Developer",
        "about": "Опытный разработчик на Python",
        "salary_expectation": 150000,
        "location": "Москва",
        "employment_type": "Полная",
        "experience_years": "3-6 лет",
        "skills": "Python, Django, FastAPI",
        "education": "МГУ, Факультет ВМК",
        "email": "ivanov@example.com",
        "phone": "+79001234567"
    }
    
    response = client.post("/api/resumes/", json=resume_data)
    assert response.status_code == 201
    data = response.json()
    assert data["full_name"] == resume_data["full_name"]
    assert data["position"] == resume_data["position"]
    assert "id" in data


def test_get_resumes(client):
    for i in range(3):
        client.post("/api/resumes/", json={
            "full_name": f"Person {i}",
            "position": f"Position {i}",
            "about": f"About {i}",
            "location": "Москва",
            "employment_type": "Полная",
            "experience_years": "1-3 года",
            "email": f"person{i}@example.com"
        })
    
    response = client.get("/api/resumes/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3


def test_get_resume_by_id(client):
    create_response = client.post("/api/resumes/", json={
        "full_name": "Test Person",
        "position": "Test Position",
        "about": "Test About",
        "location": "Москва",
        "employment_type": "Полная",
        "experience_years": "1-3 года",
        "email": "test@example.com"
    })
    resume_id = create_response.json()["id"]
    
    response = client.get(f"/api/resumes/{resume_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == resume_id
    assert data["full_name"] == "Test Person"


def test_update_resume(client):
    create_response = client.post("/api/resumes/", json={
        "full_name": "Old Name",
        "position": "Test Position",
        "about": "Test About",
        "location": "Москва",
        "employment_type": "Полная",
        "experience_years": "1-3 года",
        "email": "test@example.com"
    })
    resume_id = create_response.json()["id"]
    
    update_data = {"full_name": "New Name"}
    response = client.put(f"/api/resumes/{resume_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "New Name"


def test_delete_resume(client):
    create_response = client.post("/api/resumes/", json={
        "full_name": "Test Person",
        "position": "Test Position",
        "about": "Test About",
        "location": "Москва",
        "employment_type": "Полная",
        "experience_years": "1-3 года",
        "email": "test@example.com"
    })
    resume_id = create_response.json()["id"]
    
    response = client.delete(f"/api/resumes/{resume_id}")
    assert response.status_code == 204
    
    get_response = client.get(f"/api/resumes/{resume_id}")
    assert get_response.status_code == 404


def test_search_resumes(client):
    client.post("/api/resumes/", json={
        "full_name": "Петров Петр",
        "position": "Python Developer",
        "about": "Python specialist",
        "location": "Москва",
        "employment_type": "Полная",
        "experience_years": "1-3 года",
        "skills": "Python, Django",
        "email": "petrov@example.com"
    })
    
    client.post("/api/resumes/", json={
        "full_name": "Сидоров Сидор",
        "position": "Java Developer",
        "about": "Java specialist",
        "location": "Санкт-Петербург",
        "employment_type": "Удаленная",
        "experience_years": "3-6 лет",
        "skills": "Java, Spring",
        "email": "sidorov@example.com"
    })
    
    response = client.get("/api/resumes/search/?query=Python")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert "Python" in data[0]["position"]
    
    response = client.get("/api/resumes/search/?location=Санкт-Петербург")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["location"] == "Санкт-Петербург"


def test_vacancy_validation(client):
    response = client.post("/api/vacancies/", json={
        "title": "",
        "company": "Test",
        "description": "Test Description",
        "location": "Москва",
        "employment_type": "Полная",
        "experience": "1-3 года"
    })
    assert response.status_code == 422


def test_resume_validation(client):
    response = client.post("/api/resumes/", json={
        "full_name": "Test Person",
        "position": "Test Position",
        "about": "Test About",
        "location": "Москва",
        "employment_type": "Полная",
        "experience_years": "1-3 года",
        "email": "invalid-email"
    })
    assert response.status_code == 422
