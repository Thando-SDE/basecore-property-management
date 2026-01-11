# 🧠 Engineering Decisions – BaseCore

This document explains the key technical decisions made during development of the BaseCore Property Management System. Each choice reflects a balance between best practices, project requirements, and practical constraints, shaped by real production deployment experience.

---

## 🎯 Why Django REST Framework?

**Problem:** Needed a robust, maintainable framework to build a production-ready REST API with proper authentication and documentation.

**Solution:** Chose Django REST Framework (DRF) as the primary API framework.

- **Maturity & Adoption:** Industry-standard for Django APIs with extensive documentation
- **Authentication & Permissions:** Built-in support for multiple auth methods (Session, Token, JWT)
- **Serialization & Validation:** Strong data validation and transformation layer
- **Browseable API:** Developer-friendly interface for testing and documentation
- **Clear Architecture:** Separation of models, serializers, views, and URLs

**Outcome:** Rapid development of 15+ REST endpoints with consistent patterns and built-in security features.

---

## 🔐 Why JWT Authentication?

**Problem:** Needed stateless, scalable authentication for a REST API that could support multiple client types (web, mobile, third-party).

**Solution:** Implemented JWT (JSON Web Tokens) using `djangorestframework-simplejwt`.

- **Stateless Design:** No server-side session storage, enabling horizontal scaling
- **Frontend Compatibility:** Works seamlessly with React, Vue, Angular, and mobile clients
- **Industry Standard:** Widely adopted with good library support across ecosystems
- **Token-based Flow:** Access/refresh token pattern for security and user experience
- **Production Ready:** Successfully debugged and deployed endpoints (`/api/token/`, `/api/token/refresh/`)

**Lesson Learned:** JWT endpoints require explicit URL registration in production; silent configuration failures can occur when moving from development to production environments.

---

## 🗄️ Why PostgreSQL?

**Problem:** Required a reliable, production-grade database with strong relational integrity for property management data.

**Solution:** Selected PostgreSQL as the primary database.

- **Relational Integrity:** Foreign key constraints, transactions, ACID compliance
- **Production Reliability:** Battle-tested in enterprise environments
- **Django Integration:** Excellent Django ORM support with advanced features
- **Railway Integration:** Seamless managed PostgreSQL on deployment platform
- **Data Consistency:** Ensures property-tenant-lease-payment relationships remain valid

**Outcome:** Robust data persistence with proper constraints, surviving application restarts and deployments.

---

## 🚀 Why Railway for Deployment?

**Problem:** Needed a straightforward deployment platform that handled infrastructure (PostgreSQL, SSL, scaling) with minimal DevOps overhead.

**Solution:** Deployed on Railway.app for its developer-friendly workflow.

- **Managed Services:** PostgreSQL database, SSL certificates, load balancing
- **Simple CI/CD:** Git-based deployments with automatic builds
- **Environment Variables:** Secure secret management for production credentials
- **Scaling:** Automatic scaling based on traffic (though not heavily tested)
- **Cost:** Free tier suitable for portfolio projects with production features

**Outcome:** Zero-downtime deployments, managed database backups, and HTTPS by default.

---

## ⚙️ Why Split Settings Files?

**Problem:** Needed to maintain different configurations for development (local) and production (Railway) environments without code duplication.

**Solution:** Implemented a three-tier settings architecture:

```
settings/
├── base.py          # Shared settings (INSTALLED_APPS, MIDDLEWARE, etc.)
├── development.py   # Local dev (DEBUG=True, SQLite, localhost)
└── production.py    # Railway production (DEBUG=False, PostgreSQL, Railway domains)
```

**Benefits:**

- **Security:** Prevents accidental DEBUG=True in production
- **Clarity:** Clear separation between environment configurations
- **Maintainability:** Common settings in base, environment-specific overrides
- **Deployment Safety:** Production settings explicitly disable development features

**Critical Fix:** Had to explicitly set `WSGI_APPLICATION` in production settings to resolve deployment issues.

---

## ⚖️ Trade-offs & Scope Decisions

**Conscious decisions made to ship a working v1.0:**

### 1. No Redis Caching (Planned for Phase 3)

- **Decision:** Prioritized core functionality over performance optimizations
- **Impact:** API responses may be slower under high load
- **Future:** Redis integration planned for frequently accessed data

### 2. Limited Automated Tests (To Be Implemented)

- **Decision:** Focused on manual testing and production deployment first
- **Impact:** Higher risk of regression without test suite
- **Future:** pytest test suite planned as next priority

### 3. No Async Background Jobs

- **Decision:** Kept synchronous request/response pattern for simplicity
- **Impact:** Long-running operations block API responses
- **Future:** Celery integration planned for emails, reports, notifications

### 4. Basic Error Handling

- **Decision:** Used Django/DRF default error responses
- **Impact:** Less user-friendly error messages
- **Future:** Custom exception handlers and structured error responses

These trade-offs allowed shipping a **working production system** rather than getting stuck in "perfect but incomplete" development.

---

## 🐛 Lessons Learned from Production Debugging

### Issue 1: Silent URL Configuration Failures

- **Problem:** JWT endpoints (`/api/token/`) returned 404 in production but worked locally
- **Root Cause:** Production `urls.py` configuration didn't include JWT routes; environment-specific import issues
- **Solution:** 
  - Added explicit URL pattern logging in production
  - Created diagnostic endpoints to verify URL registration
  - Fixed import chains and middleware ordering
- **Lesson:** Always verify production URL routing independently; local success ≠ production success

### Issue 2: Static File Serving in Production

- **Problem:** Django Admin showed raw HTML instead of styled interface
- **Root Cause:** WhiteNoise middleware misconfiguration and incorrect STATIC_ROOT paths
- **Solution:**
  - Corrected `STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')` 
  - Fixed WhiteNoise middleware order in settings
  - Added Railway build command for collectstatic
- **Lesson:** Production static files require explicit configuration and testing

### Issue 3: Environment Configuration Differences

- **Problem:** Settings that worked locally failed in production
- **Root Cause:** Assumed environment parity; production had different constraints
- **Solution:**
  - Added environment detection and logging
  - Created separate production-specific configuration
  - Tested with production-like settings locally
- **Lesson:** Treat production as a distinct environment with its own requirements

---

## 🔮 Architecture Evolution

### Current State (v1.1):

- Monolithic Django application
- REST API with JWT authentication  
- PostgreSQL with relational schema
- Railway deployment with managed services

### Next Phase Considerations:

1. **Service Separation:** Split into auth service, property service, payment service
2. **Caching Layer:** Redis for frequent queries and session storage
3. **Async Workers:** Celery for background jobs (emails, reports)
4. **API Gateway:** For future microservices architecture
5. **Monitoring:** Structured logging, metrics, and alerts

**Guiding Principle:** Start simple, deploy often, evolve based on actual needs rather than anticipated complexity.

---

*Document updated: January 2026 | Project Status: Live in Production*