# docker-task-api

# Docker Task API

A simple real-world Docker project that runs a Python Flask API with a PostgreSQL database using Docker Compose.

## Project Overview

This project demonstrates how to containerize a multi-container application using Docker.

The application includes:

- Python Flask API
- PostgreSQL database
- Docker Compose
- Docker networking
- Docker volumes
- Health checks
- Multi-stage Docker builds
- Non-root container execution

## Project Structure

```text
docker-task-api/
│
├── app.py
├── requirements.txt
├── Dockerfile
├── compose.yaml
├── .dockerignore
├── .gitignore
├── .env
└── .env.example
```

## Prerequisites

Install:

- Docker Desktop
- Git
- PowerShell or another terminal

Verify Docker:

```bash
docker --version
docker compose version
```

## Environment Variables

Create a `.env` file:

```env
POSTGRES_DB=tasks
POSTGRES_USER=taskuser
POSTGRES_PASSWORD=change-me-dev-only
```

Do not commit the `.env` file to Git.

## Build the Containers

```bash
docker compose build
```

## Start the Application

```bash
docker compose up -d
```

Check the running containers:

```bash
docker compose ps
```

## Test the API

Check the health endpoint:

```bash
curl http://localhost:8080/health
```

View existing tasks:

```bash
curl http://localhost:8080/tasks
```

Create a new task:

```bash
curl -X POST http://localhost:8080/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Learn Docker"}'
```

## View Logs

View all logs:

```bash
docker compose logs
```

Follow API logs:

```bash
docker compose logs -f api
```

Follow database logs:

```bash
docker compose logs -f db
```

## Access the Containers

Open a shell inside the API container:

```bash
docker compose exec api sh
```

Connect to PostgreSQL:

```bash
docker compose exec db psql -U taskuser -d tasks
```

View tasks directly from the database:

```sql
SELECT * FROM tasks;
```

Exit PostgreSQL:

```text
\q
```

## Docker Networking

Docker Compose creates a private network for the containers.

The API connects to PostgreSQL using:

```text
DB_HOST=db
```

The name `db` comes from the database service name in `compose.yaml`.

The API does not use `localhost` to communicate with PostgreSQL because each container has its own network environment.

## Persistent Storage

PostgreSQL data is stored in a Docker named volume.

View volumes:

```bash
docker volume ls
```

Stopping and removing the containers does not delete the database data:

```bash
docker compose down
```

To remove the containers and the database volume:

```bash
docker compose down -v
```

Warning: `-v` deletes the stored database data.

## Rebuild After Code Changes

If the application code changes:

```bash
docker compose up -d --build
```

For a completely fresh build:

```bash
docker compose build --no-cache
docker compose up -d
```

## Troubleshooting

### API container is not running

Check:

```bash
docker compose ps
```

Then inspect the logs:

```bash
docker compose logs api
```

### Database container is failing

```bash
docker compose logs db
```

### API cannot connect to PostgreSQL

Verify that:

```text
DB_HOST=db
```

is being used instead of:

```text
DB_HOST=localhost
```

Test Docker DNS from the API container:

```bash
docker compose exec api getent hosts db
```

### Application still shows old code

Rebuild the image:

```bash
docker compose up -d --build
```

### Reset the Entire Development Environment

```bash
docker compose down -v
docker compose build --no-cache
docker compose up -d
```

This deletes the existing database volume.

## Key Docker Concepts Practiced

This project demonstrates:

- Docker images
- Docker containers
- Dockerfiles
- Multi-stage builds
- Docker Compose
- Container networking
- Named volumes
- Environment variables
- Health checks
- Container logs
- Container troubleshooting
- Non-root containers
- Persistent database storage

## Architecture

```text
User
 |
 | localhost:8080
 v
+------------------+
| Flask API        |
| Docker Container |
| Port 5000        |
+--------+---------+
         |
         | db:5432
         v
+------------------+
| PostgreSQL       |
| Docker Container |
+--------+---------+
         |
         v
 PostgreSQL Volume
```

## Useful Commands

```bash
docker compose build
docker compose up -d
docker compose ps
docker compose logs
docker compose logs -f api
docker compose exec api sh
docker compose exec db psql -U taskuser -d tasks
docker volume ls
docker network ls
docker compose down
docker compose down -v
```

## What I Learned

Through this project I practiced building and running a real-world multi-container application using Docker.

I learned how to:

- Build a Docker image using a multi-stage Dockerfile
- Run multiple services using Docker Compose
- Connect containers using Docker networking
- Persist PostgreSQL data using Docker volumes
- Configure containers using environment variables
- Monitor container health
- Troubleshoot containers using logs, shell access, and network commands
- Run an application as a non-root user
- Separate application configuration from the Docker image