// API базовый URL
const API_URL = '/api/vacancies';

// Загрузка вакансий при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    loadVacancies();
});

// Загрузка всех вакансий
async function loadVacancies() {
    try {
        const response = await fetch(API_URL + '/');
        const vacancies = await response.json();
        displayVacancies(vacancies);
    } catch (error) {
        console.error('Ошибка загрузки вакансий:', error);
        showError('Не удалось загрузить вакансии');
    }
}

// Отображение вакансий
function displayVacancies(vacancies) {
    const container = document.getElementById('vacanciesList');
    
    if (vacancies.length === 0) {
        container.innerHTML = '<div class="no-results">Вакансии не найдены</div>';
        return;
    }
    
    container.innerHTML = vacancies.map(vacancy => `
        <div class="item">
            <div class="item-header">
                <div>
                    <div class="item-title">${escapeHtml(vacancy.title)}</div>
                    <div class="item-subtitle">${escapeHtml(vacancy.company)}</div>
                </div>
                <div class="item-actions">
                    <button class="btn" onclick="editVacancy(${vacancy.id})">
                        <img src="/static/images/edit.svg" alt="Edit"> Изменить
                    </button>
                    <button class="btn btn-danger" onclick="deleteVacancy(${vacancy.id})">
                        <img src="/static/images/trash.svg" alt="Delete"> Удалить
                    </button>
                </div>
            </div>
            <div class="item-body">
                <div class="item-description">${escapeHtml(vacancy.description)}</div>
                <div class="item-details">
                    ${vacancy.salary_min || vacancy.salary_max ? `
                        <div class="detail-item">
                            <img src="/static/images/ruble.svg" alt="Salary">
                            <span class="detail-label">Зарплата:</span>
                            <span class="detail-value">
                                ${vacancy.salary_min ? vacancy.salary_min.toLocaleString() : '—'} - 
                                ${vacancy.salary_max ? vacancy.salary_max.toLocaleString() : '—'} ₽
                            </span>
                        </div>
                    ` : ''}
                    <div class="detail-item">
                        <img src="/static/images/map-pin.svg" alt="Location">
                        <span class="detail-label">Местоположение:</span>
                        <span class="detail-value">${escapeHtml(vacancy.location)}</span>
                    </div>
                    <div class="detail-item">
                        <img src="/static/images/briefcase.svg" alt="Employment">
                        <span class="detail-label">Занятость:</span>
                        <span class="detail-value">${escapeHtml(vacancy.employment_type)}</span>
                    </div>
                    <div class="detail-item">
                        <img src="/static/images/award.svg" alt="Experience">
                        <span class="detail-label">Опыт:</span>
                        <span class="detail-value">${escapeHtml(vacancy.experience)}</span>
                    </div>
                </div>
                ${vacancy.skills ? `
                    <div class="tags">
                        ${vacancy.skills.split(',').map(skill => 
                            `<span class="tag">${escapeHtml(skill.trim())}</span>`
                        ).join('')}
                    </div>
                ` : ''}
            </div>
        </div>
    `).join('');
}

// Поиск вакансий с фильтрами
async function searchVacancies() {
    const params = new URLSearchParams();
    
    const query = document.getElementById('searchQuery').value;
    const location = document.getElementById('locationFilter').value;
    const employmentType = document.getElementById('employmentTypeFilter').value;
    const experience = document.getElementById('experienceFilter').value;
    const salaryMin = document.getElementById('salaryMinFilter').value;
    const salaryMax = document.getElementById('salaryMaxFilter').value;
    
    if (query) params.append('query', query);
    if (location) params.append('location', location);
    if (employmentType) params.append('employment_type', employmentType);
    if (experience) params.append('experience', experience);
    if (salaryMin) params.append('salary_min', salaryMin);
    if (salaryMax) params.append('salary_max', salaryMax);
    
    try {
        const response = await fetch(API_URL + '/search/?' + params.toString());
        const vacancies = await response.json();
        displayVacancies(vacancies);
    } catch (error) {
        console.error('Ошибка поиска:', error);
        showError('Ошибка при выполнении поиска');
    }
}

// Сброс фильтров
function resetFilters() {
    document.getElementById('searchQuery').value = '';
    document.getElementById('locationFilter').value = '';
    document.getElementById('employmentTypeFilter').value = '';
    document.getElementById('experienceFilter').value = '';
    document.getElementById('salaryMinFilter').value = '';
    document.getElementById('salaryMaxFilter').value = '';
    loadVacancies();
}

// Показать форму создания вакансии
function showCreateVacancyForm() {
    document.getElementById('modalTitle').textContent = 'Добавить вакансию';
    document.getElementById('vacancyForm').reset();
    document.getElementById('vacancyId').value = '';
    document.getElementById('vacancyModal').style.display = 'block';
}

// Редактирование вакансии
async function editVacancy(id) {
    try {
        const response = await fetch(API_URL + `/${id}`);
        const vacancy = await response.json();
        
        document.getElementById('modalTitle').textContent = 'Редактировать вакансию';
        document.getElementById('vacancyId').value = vacancy.id;
        document.getElementById('title').value = vacancy.title;
        document.getElementById('company').value = vacancy.company;
        document.getElementById('description').value = vacancy.description;
        document.getElementById('salary_min').value = vacancy.salary_min || '';
        document.getElementById('salary_max').value = vacancy.salary_max || '';
        document.getElementById('location').value = vacancy.location;
        document.getElementById('employment_type').value = vacancy.employment_type;
        document.getElementById('experience').value = vacancy.experience;
        document.getElementById('skills').value = vacancy.skills || '';
        
        document.getElementById('vacancyModal').style.display = 'block';
    } catch (error) {
        console.error('Ошибка загрузки вакансии:', error);
        showError('Не удалось загрузить вакансию');
    }
}

// Удаление вакансии
async function deleteVacancy(id) {
    if (!confirm('Вы уверены, что хотите удалить эту вакансию?')) {
        return;
    }
    
    try {
        const response = await fetch(API_URL + `/${id}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            loadVacancies();
        } else {
            showError('Не удалось удалить вакансию');
        }
    } catch (error) {
        console.error('Ошибка удаления:', error);
        showError('Ошибка при удалении вакансии');
    }
}

// Обработка отправки формы
document.getElementById('vacancyForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const vacancyId = document.getElementById('vacancyId').value;
    const formData = {
        title: document.getElementById('title').value,
        company: document.getElementById('company').value,
        description: document.getElementById('description').value,
        salary_min: parseFloat(document.getElementById('salary_min').value) || null,
        salary_max: parseFloat(document.getElementById('salary_max').value) || null,
        location: document.getElementById('location').value,
        employment_type: document.getElementById('employment_type').value,
        experience: document.getElementById('experience').value,
        skills: document.getElementById('skills').value || null
    };
    
    try {
        const url = vacancyId ? API_URL + `/${vacancyId}` : API_URL + '/';
        const method = vacancyId ? 'PUT' : 'POST';
        
        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        if (response.ok) {
            closeModal();
            loadVacancies();
        } else {
            const error = await response.json();
            showError(error.detail || 'Ошибка при сохранении вакансии');
        }
    } catch (error) {
        console.error('Ошибка сохранения:', error);
        showError('Ошибка при сохранении вакансии');
    }
});

// Закрыть модальное окно
function closeModal() {
    document.getElementById('vacancyModal').style.display = 'none';
}

// Закрытие модального окна при клике вне его
window.onclick = function(event) {
    const modal = document.getElementById('vacancyModal');
    if (event.target == modal) {
        closeModal();
    }
}

// Экранирование HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Показать ошибку
function showError(message) {
    alert(message);
}
