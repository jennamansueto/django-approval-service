# Approval & Sign-Off Workflow Service

An application for managing approval workflows for deliverables in an enterprise environment.

## Tech Stack

- **Backend**: Django 3.2, Django REST Framework, PostgreSQL
- **Frontend**: Vue 3, Vite, Pinia, Vue Router
- **Testing**: pytest (backend), Vitest (frontend)
- **Infrastructure**: Docker, Docker Compose

## Quick Start

### Prerequisites

- Docker and Docker Compose installed
- Node.js 18+ (for local frontend development)

### Running with Docker

```bash
# Start all services
docker compose up --build

# Run database migrations
docker compose exec backend python manage.py migrate

# Seed sample data
docker compose exec backend python manage.py seed_data
```

The application will be available at:
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000/api
- **Django Admin**: http://localhost:8000/admin

### Sample Credentials

After running `seed_data`:

| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | Admin |
| planner | planner123 | Planner |
| approver | approver123 | Approver |
| viewer | viewer123 | Viewer |

## API Endpoints

| Endpoint | Methods | Description |
|----------|---------|-------------|
| `/api/auth/login/` | POST | User login |
| `/api/auth/logout/` | POST | User logout |
| `/api/auth/me/` | GET | Current user info |
| `/api/clients/` | GET, POST, PUT, DELETE | Client CRUD |
| `/api/deliverables/` | GET, POST, PUT, DELETE | Deliverable CRUD |
| `/api/deliverables/{id}/submit/` | POST | Submit for approval |
| `/api/approvals/` | GET | List approval requests |
| `/api/approvals/{id}/approve/` | POST | Approve request |
| `/api/approvals/{id}/reject/` | POST | Reject request |
| `/api/audit/` | GET | Audit log (read-only) |

## Running Tests

### Backend

```bash
docker compose exec backend pytest --cov=. --cov-report=term-missing
```

### Frontend

```bash
cd frontend
npm install
npm test
```

## Project Structure

```
├── backend/
│   ├── accounts/       # User model, auth views
│   ├── clients/        # Client model and API
│   ├── deliverables/   # Deliverable model and API
│   ├── approvals/      # Approval workflow
│   ├── audit/          # Audit logging
│   └── config/         # Django settings
├── frontend/
│   ├── src/
│   │   ├── api/        # API client
│   │   ├── components/ # Reusable components
│   │   ├── stores/     # Pinia stores
│   │   └── views/      # Page components
│   └── ...
└── docker-compose.yml
```

## Known Issues & Future Improvements

1. **No CSRF handling in frontend** - Session auth works but CSRF token not passed
2. **No pagination** - API returns all results
3. **No input validation messages** - Form errors not displayed to user
4. **No route guards** - Unauthenticated users can access protected routes

## License

MIT
