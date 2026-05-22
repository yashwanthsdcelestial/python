# 🎓 Online Exam Management System — Backend

A production-grade **FastAPI + PostgreSQL** backend for managing the complete lifecycle of online examinations — authentication, exam creation, student enrollment, timed attempts, auto-scoring, and result history.

---

## 📐 Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        FastAPI App                          │
│  ┌──────────┐  ┌──────────┐  ┌─────────────┐  ┌────────┐  │
│  │  /auth   │  │  /exams  │  │/enrollments │  │/admin  │  │
│  └────┬─────┘  └────┬─────┘  └──────┬──────┘  └───┬────┘  │
│       │              │               │              │       │
│  ┌────▼──────────────▼───────────────▼──────────────▼────┐  │
│  │                    Services Layer                      │  │
│  │   AuthService  ExamService  AttemptService  ...       │  │
│  └────────────────────────┬───────────────────────────────┘  │
│                           │                                  │
│  ┌────────────────────────▼───────────────────────────────┐  │
│  │                  Repository Layer                       │  │
│  │  UserRepo  ExamRepo  EnrollmentRepo  AttemptRepo       │  │
│  └────────────────────────┬───────────────────────────────┘  │
│                           │                                  │
│  ┌────────────────────────▼───────────────────────────────┐  │
│  │            PostgreSQL (SQLAlchemy ORM)                  │  │
│  │  users  exams  exam_registrations  exam_attempts        │  │
│  │  student_answers   vw_student_exam_summary (VIEW)       │  │
│  └────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🗃️ Database ER Diagram

```
users
 ├── id (PK)
 ├── email (UNIQUE)
 ├── hashed_password
 ├── full_name
 ├── role  [admin | student]
 └── is_active, is_deleted, created_at

exams
 ├── id (PK)
 ├── title, description
 ├── duration_minutes, total_marks, pass_percentage
 ├── status  [draft | published | archived]
 ├── questions  (JSON array)
 ├── max_attempts
 ├── start_time, end_time
 └── created_by (FK → users)

exam_registrations              ← many-to-many: users ↔ exams
 ├── id (PK)
 ├── student_id (FK → users)
 ├── exam_id   (FK → exams)
 └── registered_at, is_active

exam_attempts                   ← one-to-many: users → attempts
 ├── id (PK)
 ├── student_id (FK → users)
 ├── exam_id   (FK → exams)
 ├── status  [in_progress | submitted | timed_out]
 ├── score, percentage, passed
 ├── started_at, submitted_at, time_taken_seconds
 └── attempt_number

student_answers                 ← one-to-many: attempts → answers
 ├── id (PK)
 ├── attempt_id (FK → exam_attempts)
 ├── question_id
 ├── selected_answer
 ├── is_correct
 └── marks_awarded

VIEW: vw_student_exam_summary
 └── Aggregates per student per exam: best_score, ever_passed, total_attempts
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI 0.115 (Python 3.12) |
| ORM | SQLAlchemy 2.0 |
| Migrations | Alembic |
| Database | PostgreSQL 16 |
| Auth | JWT (access + refresh) via python-jose |
| Password | bcrypt via passlib |
| Validation | Pydantic v2 |
| Rate Limiting | slowapi |
| Testing | pytest + pytest-cov |
| Linting | ruff + black |

---

## 🚀 Quick Start

### Local Setup

#### Prerequisites
- Python 3.12+
- PostgreSQL 16 running locally

#### Steps

```bash
# 1. Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
copy .env.example .env
# Edit .env — set DATABASE_URL and SECRET_KEY

# 4. Run migrations
alembic upgrade head

# 5. Seed the database
python seed.py

# 6. Start the server
uvicorn app.main:app --reload --port 8000
```

API will be available at: http://localhost:8000  
Swagger docs: http://localhost:8000/docs

---

## 🔐 Sample Login Credentials (after seeding)

| Role | Email | Password |
|---|---|---|
| Admin | admin@examportal.com | Admin@1234 |
| Admin | proctor@examportal.com | Admin@1234 |
| Student | student1@example.com | Student@1234 |
| Student | student2@example.com | Student@1234 |
| Student | student3@example.com | Student@1234 |

---

## 🌐 API Overview

| Method | Endpoint | Auth | Role | Description |
|---|---|---|---|---|
| POST | /api/auth/register | ❌ | Any | Register new user |
| POST | /api/auth/login | ❌ | Any | Login, get JWT tokens |
| POST | /api/auth/refresh | ❌ | Any | Refresh access token |
| GET | /api/auth/me | ✅ | Any | Get current user |
| GET | /api/exams | ✅ | Any | List exams (students: published only) |
| GET | /api/exams/{id} | ✅ | Any | Get exam detail |
| POST | /api/exams | ✅ | Admin | Create exam |
| PUT | /api/exams/{id} | ✅ | Admin | Update exam |
| DELETE | /api/exams/{id} | ✅ | Admin | Soft-delete exam |
| POST | /api/enrollments/{exam_id} | ✅ | Student | Enroll in exam |
| GET | /api/enrollments | ✅ | Student | My enrolled exams |
| POST | /api/attempts/start/{exam_id} | ✅ | Student | Start exam attempt |
| POST | /api/attempts/{id}/submit | ✅ | Student | Submit answers |
| GET | /api/attempts/my-results | ✅ | Student | My results (paginated) |
| GET | /api/attempts/{id} | ✅ | Student | Get attempt detail |
| GET | /api/admin/stats | ✅ | Admin | Dashboard statistics |
| GET | /api/admin/users | ✅ | Admin | List all users |
| PATCH | /api/admin/users/{id}/deactivate | ✅ | Admin | Deactivate user |
| GET | /api/admin/exam-results/{id} | ✅ | Admin | All results for an exam |
| GET | /api/admin/view/student-exam-summary | ✅ | Admin | Query DB view |

Full interactive docs: http://localhost:8000/docs

---

## 🧪 Running Tests

```bash
# All tests with coverage report
pytest app/tests/ -v --cov=app --cov-report=term-missing

# Minimum 60% coverage target
pytest --cov=app --cov-fail-under=60
```

---

## ✅ Code Quality

```bash
# Lint
ruff check .

# Format check
black --check .

# Auto-format
black .
```

---

## 📦 Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| DATABASE_URL | ✅ | — | PostgreSQL connection string |
| SECRET_KEY | ✅ | — | JWT signing secret (min 32 chars) |
| ALGORITHM | ❌ | HS256 | JWT algorithm |
| ACCESS_TOKEN_EXPIRE_MINUTES | ❌ | 30 | Access token TTL |
| REFRESH_TOKEN_EXPIRE_DAYS | ❌ | 7 | Refresh token TTL |
| ALLOWED_ORIGINS | ❌ | localhost | CORS allowed origins (JSON list) |
| SMTP_USER | ❌ | — | Email — leave blank to skip |
| SMTP_PASSWORD | ❌ | — | Email password |
| DEBUG | ❌ | false | Enable debug mode |

---

## 📋 Requirements Coverage

| Requirement | Status |
|---|---|
| FastAPI + Python | ✅ |
| PostgreSQL + 5 tables | ✅ |
| Many-to-many (users ↔ exams) | ✅ |
| One-to-many (users → attempts) | ✅ |
| Database VIEW (vw_student_exam_summary) | ✅ |
| Alembic migrations (create + alter) | ✅ |
| Indexes on FK and lookup columns | ✅ |
| Seed script | ✅ |
| JWT auth (access + refresh tokens) | ✅ |
| RBAC — Admin / Student | ✅ |
| Password hashing (bcrypt) | ✅ |
| Full CRUD on exams | ✅ |
| Background Tasks (enrollment + result emails) | ✅ |
| Pagination on list endpoints | ✅ |
| Filtering + sorting on exams | ✅ |
| SOLID / layered architecture | ✅ |
| Dependency Injection | ✅ |
| Pydantic schemas — no raw ORM | ✅ |
| Structured logging + request middleware | ✅ |
| CORS configured | ✅ |
| Secrets from env vars | ✅ |
| Rate limiting on auth endpoints | ✅ |
| OpenAPI docs with tags/descriptions | ✅ |
| Postman collection | ✅ |
| pytest tests (services + API integration) | ✅ |
| ruff + black configured | ✅ |
| .gitignore | ✅ |
| Soft deletes (users + exams) | ✅ |
