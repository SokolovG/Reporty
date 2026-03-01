# Reporty

A backend-heavy reporting automation system that turns raw developer notes into structured, business-readable reports using AI. Built as a full-stack personal project to explore modern Python architecture patterns in a real-world context.

---

## The Problem

At the end of a workday, developers often struggle to translate what they actually did into language that matters to management. "Fixed auth bug" becomes a forgotten detail instead of "Resolved critical authentication issue preventing user access." Reporty automates that translation — you write quick notes throughout the day, and the system handles the rest.

---

## What It Does

- Record brief technical notes as you work
- Process them through an AI provider (configurable — OpenAI, Groq, local LLM via Ollama)
- Review and approve the AI-generated descriptions
- Generate daily reports that can be shared directly with stakeholders
- Link records to external tasks (Jira, Asana — architecture in place)

---

## Architecture

The project follows Clean Architecture with a strict separation between layers. The goal was to build something where the domain logic has zero knowledge of the database, the HTTP framework, or any external service.

```
backend/src/
├── domain/              # Entities, value objects, domain exceptions
│   ├── entities/        # DailyRecord, Report, User, ExternalTask, ...
│   └── exceptions/      # Domain-specific errors (RecordAlreadyApproved, etc.)
│
├── application/         # Use cases and ports
│   ├── use_cases/       # Orchestration logic, one class per feature group
│   ├── ports/           # Abstract repository interfaces (Protocols)
│   └── dto/             # Data transfer objects between layers
│
├── infrastructure/      # Everything external
│   ├── database/        # SQLAlchemy models, repositories, Adaptix converters
│   ├── encryption/      # Fernet encryption for API keys, JWT service
│   ├── di/              # Dishka dependency injection container
│   └── config/          # Settings, plugins, SQLAdmin
│
└── presentation/        # HTTP layer
    ├── controllers/     # Litestar route handlers
    ├── middleware/       # JWT authentication, error handling
    └── dto/             # Request/response schemas (msgspec)
```

**Key architectural decisions:**

- **Dependency Inversion** — use cases depend on `Protocol` interfaces defined in `application/ports/`, not on concrete repository implementations. The DI container wires everything together at runtime.
- **Domain entities are pure Python dataclasses** — no ORM decorators, no framework dependencies. Business rules live in methods like `record.approve()`, `record.mark_as_processed()`, `user.configure_ai()`.
- **Adaptix for object mapping** — converts between ORM models and domain entities without manual field assignment. Handles enum coercion between string storage and typed value objects.
- **Separate request/response DTOs** — msgspec Structs for validation at the HTTP boundary, completely decoupled from application DTOs.

---

## Tech Stack

**Backend**

| Technology | Role |
|---|---|
| Python 3.12 | Language |
| Litestar 2.16+ | Async web framework |
| SQLAlchemy 2.0 | ORM (async) |
| PostgreSQL | Primary database |
| Alembic | Schema migrations |
| Dishka | Dependency injection |
| msgspec | Request validation and serialization |
| Adaptix | Object mapping between layers |
| PyJWT + cryptography | RS256 JWT authentication |
| Fernet (cryptography) | API key encryption at rest |
| bcrypt | Password hashing |
| SQLAdmin | Admin panel |
| Ruff + ty | Linting and type checking |

**Frontend**

| Technology | Role |
|---|---|
| SvelteKit | Full-stack frontend framework |
| Svelte 5 | UI with runes-based reactivity |
| TailwindCSS 4 | Styling |
| jose | JWT verification on the server side |

**Infrastructure**

| Technology | Role |
|---|---|
| Docker + Docker Compose | Containerization |
| uv | Dependency management |
| pre-commit | Code quality hooks |

---

## Authentication

Custom JWT implementation using RS256 asymmetric encryption. The system issues short-lived access tokens (15 minutes) and long-lived refresh tokens (7 days) stored as HTTP-only cookies. Token rotation is handled transparently in the SvelteKit layout server — if an access token is expired, it attempts refresh before redirecting to login.

Logout blacklists both tokens server-side. Password validation enforces length, case, and digit requirements.

API keys for AI providers are stored encrypted using Fernet symmetric encryption with a master key from environment variables — they are never stored in plaintext.

---

## Running Locally

**Prerequisites:** Docker, Docker Compose

1. Clone the repository
```bash
git clone https://github.com/SokolovG/Reporty
cd reporty
```

2. Create the environment file at `backend/.env.local`:
```env
DB_HOST=db
DB_PORT=5432
DB_NAME=reporty
DB_USER=postgres
DB_PASSWORD=your_password
DEBUG=True
SECRET_KEY=your_secret_key
MASTER_ENCRYPTION_KEY=your_fernet_key  # generate with: Fernet.generate_key()
JWT_PUBLIC_KEY="-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----"
JWT_PRIVATE_KEY="-----BEGIN RSA PRIVATE KEY-----\n...\n-----END RSA PRIVATE KEY-----"
```

3. Start the stack:
```bash
docker compose up --build
```

4. Run migrations and create an admin user:
```bash
make migrate
make create_admin
```

**Available at:**
- API: `http://localhost:8080`
- Swagger docs: `http://localhost:8080/schema/swagger`
- Admin panel: `http://localhost:8080/admin`
- Frontend: `http://localhost:5173` (run separately with `npm run dev`)

---

## License

MIT
