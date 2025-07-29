# Reporty

Daily reporting automation system for fintech developers.

## 🎯 Purpose

Reporty solves the problem of creating daily reports for developers. Instead of trying to remember all tasks at the end of the day and manually formatting them in business terms, the system allows you to:

- Quickly record brief notes about completed work throughout the day
- Automatically transform technical entries into professional business descriptions
- Link work to external task management systems (Bitrix24, Jira, Asana)
- Generate comprehensive daily/weekly reports for management

## 📋 Example Transformation

**Input (developer):** `"sent callback"`
**Output (for management):** `"Configured automated payment status notifications for client."`

**Input:** `"auth fix"`
**Output:** `"Resolved critical payment system access issue, preventing potential transaction losses"`

## 🏗️ Architecture

- **Backend:** Litestar + SQLAlchemy + PostgreSQL
- **Frontend:** Svelte (learning in progress)
- **AI Processing:** Any of public LLM with API KEY / local llm
- **External Integrations:** Bitrix24, Jira, Asana support

## 🛠️ Tech Stack

## Backend
- **Language**: Python 3.12+
- **Framework**: Litestar 2.16+ (async web framework)
- **Database**: PostgreSQL with SQLAlchemy 2.0 ORM
- **Migrations**: Alembic for database schema management
- **Authentication**: JWT with litestar-users plugin
- **Dependency Injection**: Dishka container
- **Validation**: MSGSPEC for fast serialization/validation
- **Admin Interface**: SQLAdmin plugin
-
## Frontend
- **Framework**: SvelteKit 5.0+ with TypeScript
- **Styling**: TailwindCSS 4.1+
- **Build Tool**: Vite 6.2+

## Development Tools
- **Code Quality**: Ruff (linting & formatting), MyPy (type checking)
- **Pre-commit**: Automated code quality checks
- **Package Management**: UV (Python), npm (Node.js)
- **Containerization**: Docker + Docker Compose

### Database Operations
```bash
# Create new migration
make migration msg="description"

# Apply migrations
make migrate

# Direct alembic commands
docker compose exec backend uv run alembic revision --autogenerate -m "message"
docker compose exec backend uv run alembic upgrade head
```
