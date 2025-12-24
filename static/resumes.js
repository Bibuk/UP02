// API базовый URL
const API_URL = '/api/resumes';

// Загрузка резюме при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    loadResumes();
});

// Загрузка всех резюме
async function loadResumes() {
    try {
        const response = await fetch(API_URL + '/');
        const resumes = await response.json();
        displayResumes(resumes);
    } catch (error) {
        console.error('Ошибка загрузки резюме:', error);
        showError('Не удалось загрузить резюме');
    }
}

// Отображение резюме
function displayResumes(resumes) {
    const container = document.getElementById('resumesList');
    
    if (resumes.length === 0) {
        container.innerHTML = '<div class="no-results">Резюме не найдены</div>';
        return;
    }
    
    container.innerHTML = resumes.map(resume => `
        <div class="item">
            <div class="item-header">
                <div>
                    <div class="item-title">${escapeHtml(resume.full_name)}</div>
                    <div class="item-subtitle">${escapeHtml(resume.position)}</div>
                </div>
                <div class="item-actions">
                    <button class="btn" onclick="editResume(${resume.id})">
                        <img src="/static/images/edit.svg" alt="Edit"> Изменить
                    </button>
                    <button class="btn btn-danger" onclick="deleteResume(${resume.id})">
                        <img src="/static/images/trash.svg" alt="Delete"> Удалить
                    </button>
                </div>
            </div>
            <div class="item-body">
                <div class="item-description">${escapeHtml(resume.about)}</div>
                <div class="item-details">
                    ${resume.salary_expectation ? `
                        <div class="detail-item">
                            <img src="/static/images/ruble.svg" alt="Salary">
                            <span class="detail-label">Ожидаемая ЗП:</span>
                            <span class="detail-value">${resume.salary_expectation.toLocaleString()} ₽</span>
                        </div>
                    ` : ''}
                    <div class="detail-item">
                        <img src="/static/images/map-pin.svg" alt="Location">
                        <span class="detail-label">Местоположение:</span>
                        <span class="detail-value">${escapeHtml(resume.location)}</span>
                    </div>
                    <div class="detail-item">
                        <img src="/static/images/briefcase.svg" alt="Employment">
                        <span class="detail-label">Занятость:</span>
                        <span class="detail-value">${escapeHtml(resume.employment_type)}</span>
                    </div>
                    <div class="detail-item">
                        <img src="/static/images/award.svg" alt="Experience">
                        <span class="detail-label">Опыт:</span>
                        <span class="detail-value">${escapeHtml(resume.experience_years)}</span>
                    </div>
                    <div class="detail-item">
                        <img src="/static/images/email.svg" alt="">
                        <span class="detail-label">Email:</span>
                        <span class="detail-value">${escapeHtml(resume.email)}</span>
                    </div>
                    ${resume.phone ? `
                        <div class="detail-item">
                            <img src="/static/images/phone.svg" alt="">
                            <span class="detail-label">Телефон:</span>
                            <span class="detail-value">${escapeHtml(resume.phone)}</span>
                        </div>
                    ` : ''}
                    ${resume.education ? `
                        <div class="detail-item">
                            <img src="/static/images/graduation.svg" alt="">
                            <span class="detail-label">Образование:</span>
                            <span class="detail-value">${escapeHtml(resume.education)}</span>
                        </div>
                    ` : ''}
                </div>
                ${resume.skills ? `
                    <div class="tags">
                        ${resume.skills.split(',').map(skill => 
                            `<span class="tag">${escapeHtml(skill.trim())}</span>`
                        ).join('')}
                    </div>
                ` : ''}
            </div>
        </div>
    `).join('');
}

// Поиск резюме с фильтрами
async function searchResumes() {
    const params = new URLSearchParams();
    
    const query = document.getElementById('searchQuery').value;
    const location = document.getElementById('locationFilter').value;
    const employmentType = document.getElementById('employmentTypeFilter').value;
    const experienceYears = document.getElementById('experienceFilter').value;
    const salaryMin = document.getElementById('salaryMinFilter').value;
    const salaryMax = document.getElementById('salaryMaxFilter').value;
    
    if (query) params.append('query', query);
    if (location) params.append('location', location);
    if (employmentType) params.append('employment_type', employmentType);
    if (experienceYears) params.append('experience_years', experienceYears);
    if (salaryMin) params.append('salary_min', salaryMin);
    if (salaryMax) params.append('salary_max', salaryMax);
    
    try {
        const response = await fetch(API_URL + '/search/?' + params.toString());
        const resumes = await response.json();
        displayResumes(resumes);
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
    loadResumes();
}

// Показать форму создания резюме
function showCreateResumeForm() {
    document.getElementById('modalTitle').textContent = 'Добавить резюме';
    document.getElementById('resumeForm').reset();
    document.getElementById('resumeId').value = '';
    document.getElementById('resumeModal').style.display = 'block';
}

// Редактирование резюме
async function editResume(id) {
    try {
        const response = await fetch(API_URL + `/${id}`);
        const resume = await response.json();
        
        document.getElementById('modalTitle').textContent = 'Редактировать резюме';
        document.getElementById('resumeId').value = resume.id;
        document.getElementById('full_name').value = resume.full_name;
        document.getElementById('position').value = resume.position;
        document.getElementById('about').value = resume.about;
        document.getElementById('salary_expectation').value = resume.salary_expectation || '';
        document.getElementById('location').value = resume.location;
        document.getElementById('employment_type').value = resume.employment_type;
        document.getElementById('experience_years').value = resume.experience_years;
        document.getElementById('skills').value = resume.skills || '';
        document.getElementById('education').value = resume.education || '';
        document.getElementById('email').value = resume.email;
        document.getElementById('phone').value = resume.phone || '';
        
        document.getElementById('resumeModal').style.display = 'block';
    } catch (error) {
        console.error('Ошибка загрузки резюме:', error);
        showError('Не удалось загрузить резюме');
    }
}

// Удаление резюме
async function deleteResume(id) {
    if (!confirm('Вы уверены, что хотите удалить это резюме?')) {
        return;
    }
    
    try {
        const response = await fetch(API_URL + `/${id}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            loadResumes();
        } else {
            showError('Не удалось удалить резюме');
        }
    } catch (error) {
        console.error('Ошибка удаления:', error);
        showError('Ошибка при удалении резюме');
    }
}

// Обработка отправки формы
document.getElementById('resumeForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const resumeId = document.getElementById('resumeId').value;
    const formData = {
        full_name: document.getElementById('full_name').value,
        position: document.getElementById('position').value,
        about: document.getElementById('about').value,
        salary_expectation: parseFloat(document.getElementById('salary_expectation').value) || null,
        location: document.getElementById('location').value,
        employment_type: document.getElementById('employment_type').value,
        experience_years: document.getElementById('experience_years').value,
        skills: document.getElementById('skills').value || null,
        education: document.getElementById('education').value || null,
        email: document.getElementById('email').value,
        phone: document.getElementById('phone').value || null
    };
    
    try {
        const url = resumeId ? API_URL + `/${resumeId}` : API_URL + '/';
        const method = resumeId ? 'PUT' : 'POST';
        
        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        if (response.ok) {
            closeModal();
            loadResumes();
        } else {
            const error = await response.json();
            showError(error.detail || 'Ошибка при сохранении резюме');
        }
    } catch (error) {
        console.error('Ошибка сохранения:', error);
        showError('Ошибка при сохранении резюме');
    }
});

// Закрыть модальное окно
function closeModal() {
    document.getElementById('resumeModal').style.display = 'none';
}

// Закрытие модального окна при клике вне его
window.onclick = function(event) {
    const modal = document.getElementById('resumeModal');
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
