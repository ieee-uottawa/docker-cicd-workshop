# Python Docker + CI/CD Workshop App

[![Python CI](https://github.com/ieee-uottawa/docker-cicd-workshop/actions/workflows/ci.yaml/badge.svg)](https://github.com/ieee-uottawa/docker-cicd-workshop/actions/workflows/ci.yaml)

A minimal Python web server project for learning Docker and GitHub Actions CI/CD.

## What this app does

- Runs a Flask web server on port `8000`.
- Exposes health and demo endpoints.
- Fetches your public IP address from `https://api.ipify.org` through an API route.
- Includes a simple `add(a, b)` function used by tests.

## Project structure

```text
.
├── .env
├── .github/
│   └── workflows/
│       ├── ci.yaml
│       └── cd.yaml
├── Dockerfile
├── app.py
├── docker-compose.yml
├── requirements.txt
├── secrets/
│   └── demo_secret.txt
├── test_app.py
└── venv/
```

## Prerequisites

- Python 3.10+
- pip
- Docker

## Local setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run the app

```bash
python app.py
```

Server URL:

- `http://localhost:8000`

Available endpoints:

- `GET /` → welcome message
- `GET /health` → health check
- `GET /ip` → fetches public IP via external API
- `GET /add?a=2&b=3` → returns sum
- `GET /config` → shows minimal env-based config and secret status

## Environment variables (`.env`)

This project includes a minimal example `.env` file.

Note: `.env` is loaded automatically by Docker Compose (`env_file` in `docker-compose.yml`).
For plain local runs (`python app.py`), export variables in your shell if you want to override defaults.

Current example variables:

- `APP_PORT` (default `8000`)
- `APP_MESSAGE` (default `Docker + CI/CD workshop server`)
- `IPIFY_URL`
- `IPIFY_TIMEOUT`
- `DEMO_SECRET_FILE`

## Run tests

```bash
pytest -q
```

Current test file:

- `test_app.py`

## Lint

```bash
flake8 .
```

## Docker

Build image:

```bash
docker build -t my-python-app:latest .
```

Run container:

```bash
docker run --rm -p 8000:8000 my-python-app:latest
```

Test container endpoint:

```bash
curl http://localhost:8000/health
```

## Docker Compose + secrets

The project includes `docker-compose.yml` and mounts a demo secret from `secrets/demo_secret.txt`.

Run with compose:

```bash
docker compose up --build
```

Stop compose:

```bash
docker compose down
```

## GitHub Actions workflows

### CI workflow (`.github/workflows/ci.yaml`)

Triggers:

- Push to `main`
- Pull requests to `main`

Jobs:

1. **tests**

   - Runs on Python `3.12`, `3.13`, `3.14`
   - Installs deps
   - Runs `pytest --junitxml=test-results.xml`
   - Uploads test results artifact
2. **lint**
   - Runs `flake8 .`
3. **container-build** (depends on tests + lint)
   - Builds Docker image
   - Runs container in background
   - Checks `http://localhost:8000/health`

### CD workflow (`.github/workflows/cd.yaml`)

Trigger:

- GitHub Release published

What it does:

- Logs in to Docker Hub
- Builds image tagged with release version and `latest`
- Pushes both tags to Docker Hub

Required GitHub repository secrets:

- `DOCKER_HUB_USERNAME`
- `DOCKER_HUB_TOKEN`
- `DISCORD_TOKEN`

## Notes for workshop use

- Keep tests small and focused to show CI feedback quickly.
- Make one intentional change (for example, break `add`) to demonstrate a failing PR check.
- Use the uploaded test report artifact to show how CI stores test results.

## Troubleshooting

- **`pytest: command not found`**
  - Activate your virtual environment: `source venv/bin/activate`
  - Install dependencies: `pip install -r requirements.txt`
- **`ModuleNotFoundError: requests`**
  - Install project dependencies again: `pip install -r requirements.txt`
- **CI lint job fails**
  - Run locally to reproduce: `flake8 .`
- **Docker build fails**
  - Rebuild from a clean state: `docker build --no-cache -t my-python-app:latest .`
- **Container health check fails**
  - Ensure port mapping is set: `-p 8000:8000`
  - Check logs: `docker logs <container-name>`
- **`/ip` endpoint returns error**
  - Check host/container internet access. This route calls `https://api.ipify.org`.
