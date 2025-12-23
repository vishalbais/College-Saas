# College-Saas — Event Management SaaS (MVP v1)

This repository contains an MVP for a multi-tenant Event Management SaaS.

Tech stack
- Frontend: React + TypeScript + Vite + Tailwind CSS
- Backend: Python FastAPI (async)
- DB: PostgreSQL (SQLAlchemy async)
- Auth: JWT (roles: SuperAdmin, CollegeAdmin, Editor)
- Background jobs: Celery + Redis
- Storage: Local file storage for development (S3-compatible recommended for prod)
- Docker + docker-compose for local development

Quick start (development)
1. Copy `.env.example` to `.env` and adjust values.
2. Start services:
   docker/docker-compose.yml includes: postgres, redis, backend, frontend, celery worker.
   Run: docker compose up --build
3. Backend docs: http://localhost:8000/docs

Notes
- This is an MVP scaffold. For production:
  - Use managed Postgres, S3 (or equivalent), TLS, secrets manager.
  - Configure Celery to use a broker appropriate to scale (Redis OK; consider RabbitMQ).
  - Configure rate limiting, logging, monitoring.
  - Run migrations (Alembic) — a simple models baseline is provided.

What's included
- Authentication (signup/login), role-based dependencies
- College & event APIs, tenant isolation by college_id
- Student import (CSV, XLSX via pandas), Google Sheets import (stub requires credentials)
- QR UID generation and PNG creation via qrcode
- Ticket send via Celery task (email sending stub using SMTP)
- Check-in API supporting QR scan and manual UID
- Reporting endpoints
- Audit logging on key actions
