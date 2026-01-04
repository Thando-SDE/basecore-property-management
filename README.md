![Python](https://img.shields.io/badge/Python-3.12-blue)
![Django](https://img.shields.io/badge/Django-5.2-darkgreen)
![DRF](https://img.shields.io/badge/Django%20REST%20Framework-3.15-red)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Production-blue)
![Railway](https://img.shields.io/badge/Deployed%20on-Railway-purple)
![API](https://img.shields.io/badge/API-REST-success)
![License](https://img.shields.io/badge/License-MIT-green)

# BaseCore Property Management System

BaseCore is a **production-ready backend system** for managing properties, tenants, leases, and payments.  
It is built using **Django and Django REST Framework**, designed with **real-world backend architecture**, and deployed to **Railway with PostgreSQL**.

---

## Live Deployment

- **API Base URL:**  
  https://pleasant-happiness.up.railway.app/api/

- **Admin Dashboard:**  
  https://pleasant-happiness.up.railway.app/admin/

- **Status:** Fully deployed and operational

---

## Core Features

- JWT authentication with access and refresh tokens  
- Role-based permissions (Owner, Manager, Tenant)  
- Property management (CRUD operations)  
- Tenant profiles and history tracking  
- Lease lifecycle management  
- Payment processing and payment history  
- RESTful API design with predictable endpoints  
- Production PostgreSQL database  

---

## Technology Stack

- **Backend Framework:** Django 5.2.7  
- **API Framework:** Django REST Framework 3.15.2  
- **Authentication:** JWT (djangorestframework-simplejwt)  
- **Database:** PostgreSQL (production), SQLite (development)  
- **API Documentation:** OpenAPI / Swagger (DRF Spectacular)  
- **Deployment:** Railway.app with Gunicorn  
- **Static Files:** WhiteNoise  
- **Security:** CORS, HTTPS, secure cookies  

---

## Project Structure

```
basecore/
├── settings/
│   ├── base.py
│   ├── development.py
│   └── production.py
├── api/
├── users/
├── properties/
├── tenants/
├── leases/
├── payments/
└── manage.py
```

---

## Local Development Setup

```bash
# Clone repository
git clone https://github.com/Thando-SDE/basecore-property-management.git
cd basecore-property-management

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate      # Windows
source venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env

# Apply database migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

---

## API Documentation (Swagger)

Swagger UI is automatically generated using OpenAPI standards.

**Local:**  
http://127.0.0.1:8000/api/docs/

**Production:**  
https://pleasant-happiness.up.railway.app/api/docs/

---

## Authentication Example

```http
POST /api/token/
Content-Type: application/json

{
  "username": "admin",
  "password": "your_password"
}
```

---

## Deployment Overview

- Automatic deployment via Railway on `git push`
- PostgreSQL provisioned and managed by Railway
- Environment variables secured via dashboard
- Production settings enforced (`DEBUG=False`)
- HTTPS enabled with SSL/TLS

---

## Security Practices

- JWT authentication with token refresh
- Password hashing via Django authentication system
- Environment-based settings separation
- CORS configuration for frontend integration
- Secure cookies in production
- Encrypted database connections

---

## Development Timeline

- **Weeks 1–2:** System design, ERD, API specification
- **Week 3:** Project setup and configuration
- **Week 4:** Core models, endpoints, authentication
- **Week 5:** Deployment, testing, documentation
- **Current Status:** Live in production

---

## Author

**Thando SDE**  
ALX Backend Specialization

- **GitHub:** https://github.com/Thando-SDE
- **Live Demo:** https://pleasant-happiness.up.railway.app

---

## License

MIT License. See the [LICENSE](LICENSE) file for details.

---

**Version:** 1.0.0  
**Live Since:** January 2025