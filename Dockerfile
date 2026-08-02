# Stage 1: build the React frontend
FROM node:22-slim AS frontend-build
WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ ./
# Base path the SPA is built under. This service lives behind the shared front
# door at apps.p3mai.com/pmo, so the prod build defaults to /pmo/. (Local dev
# doesn't use this Dockerfile — Vite serves at / via vite.config's APP_BASE||'/'.)
ARG APP_BASE=/pmo/
ENV APP_BASE=$APP_BASE
RUN npm run build

# Stage 2: Python backend, serving the built frontend from Stage 1
FROM python:3.12-slim
WORKDIR /app/backend
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ ./
COPY --from=frontend-build /app/frontend/dist /app/frontend/dist

EXPOSE 8000
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
