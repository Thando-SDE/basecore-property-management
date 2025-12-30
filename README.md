# BaseCore Property Management System

A comprehensive Django-based property management system for tracking properties, tenants, leases, and payments.

## Features
- Property listing and management
- Tenant information tracking
- Lease agreement management
- Payment processing with Payment Intents
- User authentication and authorization

## Tech Stack
- **Backend**: Django 4.x, Django REST Framework
- **Database**: SQLite (development), PostgreSQL (production ready)
- **API**: RESTful endpoints
- **Authentication**: Token-based, Session-based
- **Payments**: Stripe-like payment intent system

## Project Structure
\`\`\`
basecore/
├── properties/      # Property management
├── tenants/         # Tenant management
├── leases/          # Lease agreements
├── payments/        # Payment processing
├── users/           # Authentication
└── basecore/        # Project settings
\`\`\`

## Getting Started

### Prerequisites
- Python 3.8+
- pip
- Git

### Installation
1. Clone repository:
   \`\`\`bash
   git clone https://github.com/Thando-SDE/basecore-property-management.git
   cd basecore-property-management
   \`\`\`

2. Create virtual environment:
   \`\`\`bash
   python -m venv venv
   # On Windows:
   venv\\Scripts\\activate
   # On macOS/Linux:
   source venv/bin/activate
   \`\`\`

3. Install dependencies:
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

4. Apply migrations:
   \`\`\`bash
   python manage.py migrate
   \`\`\`

5. Run development server:
   \`\`\`bash
   python manage.py runserver
   \`\`\`

6. Visit http://localhost:8000

## Development Status
- **Week 1-2**: Planning, ERD design, API planning
- **Week 3**: Initial project setup, repository configuration
- **Week 4**: Core models, API endpoints, authentication
- **Week 5**: Frontend integration, testing, deployment

## License
MIT License
