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

- **Language:** Python 3.12
- **Framework:** Litestar 2.16+
- **Database:** PostgreSQL with SQLAlchemy 2.0, Alembic
- **API:** REST with automatic OpenAPI docs
- **Auth:** JWT with litestar-users
- **Validation:** MSGSPEC
- **Code Quality:** Ruff, MyPy, Pre-commit
- **Deployment:** Docker + Docker Compose
