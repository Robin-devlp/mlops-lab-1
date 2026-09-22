# Stage 1 (builder): install the dependencies into a virtual environment with uv
FROM python:3.13-slim AS builder

RUN pip install --no-cache-dir uv==0.12.12

WORKDIR /app
# copy packages into the venv instead of linking them from the uv cache mount,
# and use the image's own Python instead of downloading another one
ENV UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never

# copy only the dependency files first, so this slow layer comes from the build
# cache as long as pyproject.toml and uv.lock don't change
COPY pyproject.toml uv.lock ./
# --no-install-project: installing the project itself needs src/, which isn't
# copied yet, and the service runs straight from src/ anyway
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-install-project


# Stage 2 (runtime): a clean slim image with only the venv and the code
FROM python:3.13-slim

WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
COPY src/ ./src/

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1

EXPOSE 8000
ENTRYPOINT ["uvicorn", "src.food11.serve:app", "--host", "0.0.0.0", "--port", "8000"]
