FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN pip install uv

ENV UV_PROJECT_ENVIRONMENT=/tmp/.venv
RUN uv sync --frozen

COPY . .

CMD ["uv", "run", "litestar", "--app", "backend.src.main:app", "run", "--host", "0.0.0.0", "--port", "8080"]
