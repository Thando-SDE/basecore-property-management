# 🏗️ BaseCore Architecture Overview

This document describes the high-level architecture and system design of the BaseCore Property Management System, including deployment architecture, data flow, and key technical decisions validated through production deployment.

---

## 🔹 System Overview

BaseCore is a **backend-first Django REST API** deployed in production on Railway, designed to manage the complete lifecycle of property management: properties, tenants, leases, and payments.

### Core Architectural Principles:

1. **Separation of Concerns:** Clear layers with distinct responsibilities
2. **Production-First:** Built for deployment, not just local development
3. **Security by Default:** HTTPS, authentication, and validation at every layer
4. **Relational Integrity:** PostgreSQL with proper foreign key relationships
5. **API-First Design:** RESTful endpoints as the primary interface

### Architecture Layers:

```
┌─────────────────────────────────┐
│     Client Applications         │ ← Web, Mobile, Third-party APIs
│ (React, Mobile Apps, etc.)      │
└──────────────┬──────────────────┘
               │ HTTPS/JSON
┌──────────────▼──────────────────┐
│   Django REST Framework         │ ← API Layer (Serializers, Views, Authentication)
│ (Request/Response Handling)     │
└──────────────┬──────────────────┘
               │ Business Logic
┌──────────────▼──────────────────┐
│    Django Models & ORM          │ ← Business Logic & Data Validation
│  (Property, Tenant, Lease,      │
│   Payment, User models)         │
└──────────────┬──────────────────┘
               │ Database Queries
┌──────────────▼──────────────────┐
│    PostgreSQL Database          │ ← Persistence Layer (Production)
│  (Relational Data Storage)      │
└─────────────────────────────────┘
```

---

## 🔹 Request Lifecycle (Production Flow)

**Complete request path from client to database and back:**

```
Client Request
    ↓ HTTPS Request (Railway Domain)
Railway Infrastructure
    ↓ Load Balancing & SSL Termination
Gunicorn WSGI Server
    ↓ Request parsing & worker allocation
Django Middleware Stack
    ↓ SecurityMiddleware → WhiteNoise → Session → Auth → etc.
URL Routing
    ↓ basecore/urls.py → App urls.py
      (Critical: JWT endpoints must be registered here)
DRF View Processing
    ↓ Authentication → Permissions → Throttling
Serializer Validation
    ↓ Input cleaning, field validation, data transformation
ORM Database Operations
    ↓ SQL generation → Connection pooling → Query execution
Response Serialization
    ↓ Python objects → JSON
Middleware (Return path)
    ↓ Response middleware processing
HTTP Response
    ↓ JSON payload + headers to client
```

**Key Production Insight:** Steps 4-5 (Middleware & URL Routing) were critical debugging points where JWT endpoints silently failed in production due to configuration mismatches.

---

## 🔹 Application Structure & Domain Design

### Monolithic Django Application with Modular Apps:

```
basecore/                    # Project root
├── users/                   # Authentication & User Management
│   ├── models.py            # Custom User model (AUTH_USER_MODEL)
│   ├── serializers.py       # UserRegistrationSerializer, UserSerializer
│   ├── views.py             # RegisterView, UserProfileView
│   └── urls.py              # /api/users/ endpoints
│
├── properties/              # Property Management
│   ├── models.py            # Property model
│   ├── serializers.py       # PropertySerializer
│   ├── views.py             # PropertyListCreateView, PropertyDetailView
│   └── urls.py              # /api/properties/ endpoints
│
├── tenants/                 # Tenant Management
│   └── (similar structure)
│
├── leases/                  # Lease Agreement Management
│   └── (similar structure)
│
└── payments/                # Payment Tracking
    └── (similar structure)
```

### Domain Relationships (Business Logic):

```
Property (1) ──── has ────▶ (Many) Lease (1) ──── has ────▶ (Many) Payment
      │                           │
      │                           │
  managed by                  signed by
      │                           │
      ▼                           ▼
User (Manager)              Tenant (Renter)
```

**Design Decision:** Each domain has its own Django app for maintainability, but all share the same database and deployment for simplicity in v1.0.

---

## 🔹 Deployment Architecture (Production)

### Railway Production Environment:

```
                            ┌─────────────────┐
                            │   GitHub Repo   │
                            │  (Source Code)  │
                            └────────┬────────┘
                                     │ Git Push
                            ┌────────▼────────┐
                            │   Railway CI/CD │
                            │  (Auto-deploy)  │
                            └────────┬────────┘
                                     │ Build & Deploy
┌──────────────┐   ┌────────▼────────┐   ┌──────────────┐
│              │   │                 │   │              │
│   Internet   │   │  Railway Proxy  │   │   Gunicorn   │
│   Clients    │───│ (Load Balancer  │───│ (4 Workers)  │
│              │   │    & SSL)       │   │              │
└──────────────┘   └────────┬────────┘   └──────┬───────┘
                            │                   │
                   ┌────────▼────────┐   ┌──────▼───────┐
                   │  Environment    │   │    Django    │
                   │   Variables     │   │ Application  │
                   │   (Secrets)     │   └──────┬───────┘
                   └─────────────────┘          │
                                         ┌──────▼───────┐
                                         │  PostgreSQL  │
                                         │  (Managed)   │
                                         └──────────────┘
```

### Key Production Components:

1. **Railway Platform:** Infrastructure as a Service (SSL, load balancing, scaling)
2. **Gunicorn:** Production WSGI server with 4 worker processes
3. **WhiteNoise:** Static file serving in production (critical for Admin CSS/JS)
4. **PostgreSQL:** Managed database with automated backups
5. **Environment Variables:** Secure configuration (DJANGO_SECRET_KEY, DATABASE_URL)

---

## 🔹 Environment Configuration Strategy

**Three-Tier Settings Architecture (Validated in Production):**

```python
# settings/base.py - Shared configuration
INSTALLED_APPS = [ ... ]
MIDDLEWARE = [ ... ]
# Common settings for ALL environments

# settings/development.py - Local Development
from .base import *
DEBUG = True
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', ...}}
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# settings/production.py - Railway Production  
from .base import *
DEBUG = False
DATABASES = {'default': dj_database_url.config(conn_max_age=600)}
ALLOWED_HOSTS = ['basecore-property-management-production.up.railway.app', ...]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Critical for production
WSGI_APPLICATION = 'basecore.wsgi.application'  # Explicitly set for production
```

### Lessons from Production Debugging:

- **Explicit WSGI_APPLICATION:** Must be set in production settings
- **Static File Configuration:** Different requirements in production vs development
- **URL Routing:** Production may have different import/registration behavior
- **Middleware Ordering:** Critical for security and functionality

---

## 🔹 Security Architecture

### Defense in Depth Approach:

```
Layer 1: Infrastructure Security
├── Railway managed HTTPS/SSL
├── Automatic security updates
└── DDoS protection (platform level)

Layer 2: Application Security  
├── Django security middleware
│   ├── SecurityMiddleware (HSTS, SSL redirect)
│   ├── Clickjacking protection
│   └── Content sniffing prevention
├── CSRF protection for state-changing operations
└── Secure headers (CSP, Referrer-Policy)

Layer 3: Authentication & Authorization
├── JWT token-based authentication
├── Permission classes on all endpoints
├── Password hashing (PBKDF2 with salt)
└── Rate limiting (planned)

Layer 4: Data Security
├── PostgreSQL with encrypted connections
├── SQL injection prevention via Django ORM
├── Input validation on all serializers
└── Environment variable secrets management
```

### Production Security Validations:

✅ All API endpoints return 401 without valid authentication  
✅ HTTPS enforced in production (no HTTP access)  
✅ DEBUG=False prevents information leakage  
✅ Admin panel accessible only to staff users  
✅ CORS configured for potential frontend integration  

---

## 🔹 Data Flow & Performance Considerations

### Typical API Request Flow:

```
1. User Registration → POST /api/users/
   ↓
2. JWT Token Request → POST /api/token/ (validates credentials)
   ↓  
3. Authenticated Request → GET /api/properties/ (with Bearer token)
   ↓
4. Database Query → SELECT * FROM properties WHERE manager_id = ?
   ↓
5. Response → JSON list of properties
```

### Performance Optimizations (Current & Planned):

- **Current:** Database indexes on foreign keys, select_related() for joins
- **Phase 2:** Query optimization, Django Debug Toolbar analysis
- **Phase 3:** Redis caching for frequent queries (property lists, user data)
- **Future:** Database connection pooling, query optimization

### Scalability Considerations:

- **Vertical Scaling:** Railway can increase resources (RAM, CPU)
- **Horizontal Scaling:** Stateless JWT allows multiple Gunicorn workers
- **Database Scaling:** PostgreSQL read replicas for heavy read loads
- **Caching Strategy:** Redis for session storage and frequent queries

---

## 🔹 Monitoring & Observability

### Current (Basic):

- Railway built-in logs and metrics
- Django logging to stdout (captured by Railway)
- Health endpoint (/) for basic uptime monitoring
- Manual verification scripts (verify_project.sh)

### Planned Improvements:

- **Structured Logging:** JSON logs with request IDs for tracing
- **Metrics Collection:** Response times, error rates, database query counts
- **Error Tracking:** Sentry integration for production errors
- **Health Checks:** Comprehensive health endpoint with dependency checks

---

## 🔹 Architecture Evolution Path

### v1.0 (Current): Monolithic Django app with clear separation of concerns

✅ Deployed and working in production  
✅ Full authentication and data model  
✅ Basic security and performance  

### v2.0 (Planned): Enhanced monolith with added services

- Redis caching layer
- Celery background workers
- Advanced search with PostgreSQL full-text search
- File upload for property images

### v3.0 (Future): Service-oriented architecture

- Separate auth microservice
- Property service with dedicated database
- Payment service with Stripe integration
- API Gateway for routing and rate limiting

**Guiding Principle:** Start with a well-structured monolith, extract services only when necessary, and always maintain a working production system.

---

*Architecture documented: January 2026 | System Status: Live in Production*