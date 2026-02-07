# ShipEngine Address Validation API

This project is a FastAPI-based microservice for validating postal addresses using the ShipEngine API. It features asynchronous processing, background job handling with ARQ and Redis, and a PostgreSQL database for address storage.

## Features

- **FastAPI** REST API for address management
- **Async SQLAlchemy** for database operations
- **ARQ** for background job processing (address validation)
- **Redis** for job queue
- **PostgreSQL** for persistent storage
- **Docker** and **docker-compose** for easy local development
- **Alembic** for database migrations

## Project Structure

```
app/
  api/v1/addresses.py      # API endpoints
  core/config.py           # App configuration
  db/                      # Database setup
  models/address.py        # SQLAlchemy models
  repositories/address.py  # Data access layer
  schemas/address.py       # Pydantic schemas
  services/                # Business logic & external API
  worker.py                # Background worker
main.py                    # FastAPI app entrypoint
worker.py                  # (duplicate, to be removed)
requirements.txt           # Python dependencies
Dockerfile                 # Docker image definition
docker-compose.yml         # Multi-container setup
migrations/                # Alembic migration scripts
```

## How to Launch

Follow these steps to launch the project locally using Docker Compose:

### 1. Clone the repository

```sh
git clone <repo-url>
cd <repo-folder>
```

### 2. Configure Environment Variables

Create a `.env` file inside the `test/` directory with the following content:

```
PROJECT_NAME=ShipEngine CRUD Service
SHIPENGINE_API_KEY=TEST_ajmhsjS6UZfp8hho/VNMqM6vP4fsGcHSVLPZgDF+4Uw
DATABASE_URL=postgresql+asyncpg://postgres:admin123@db:5432/shipengine_db
REDIS_URL=redis://redis:6379/0
```

### 3. Build and Start Services

Run the following command to build and start all services:

```sh
docker-compose up --build
```

The API will be available at: http://localhost:8000
API documentation: http://localhost:8000/docs

### 4. Apply Database Migrations

In a new terminal, run:

```sh
docker-compose exec api alembic upgrade head
```

### 5. Stopping the Services

To stop all running containers, press `Ctrl+C` in the terminal where Docker Compose is running, then run:

```sh
docker-compose down
```

---

For local development without Docker, install dependencies and run the app with Uvicorn:

```sh
pip install -r requirements.txt
uvicorn main:app --reload
```

## API Endpoints

- `POST /api/v1/addresses/` — Create and validate an address
- `GET /api/v1/addresses/` — List all addressesdo
- `GET /api/v1/addresses/{id}` — Get address by ID
- `DELETE /api/v1/addresses/{id}` — Delete address

## Background Worker

- The worker validates addresses asynchronously using ARQ and ShipEngine.
- See `app/worker.py` for implementation.

## Development

- Python 3.10+
- Install dependencies: `pip install -r requirements.txt`
- Run locally: `uvicorn main:app --reload`

## License

MIT
