import os

import psycopg

from flask import Flask, jsonify, request


app = Flask(__name__)


def get_connection():

    # Docker Compose will supply these values
    # through environment variables.

    return psycopg.connect(
        host=os.getenv("DB_HOST", "db"),
        dbname=os.getenv("DB_NAME", "tasks"),
        user=os.getenv("DB_USER", "taskuser"),
        password=os.getenv("DB_PASSWORD")
    )


def init_db():

    with get_connection() as connection:

        with connection.cursor() as cursor:

            cursor.execute("SELECT pg_advisory_xact_lock(12345, 1)")

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    completed BOOLEAN DEFAULT FALSE
                );
            """)


# Create the table when the app starts.
init_db()


@app.get("/health")
def health():

    try:

        with get_connection() as connection:

            with connection.cursor() as cursor:

                cursor.execute("SELECT 1")

        return jsonify(status="healthy"), 200

    except Exception as error:

        return jsonify(
            status="unhealthy",
            error=str(error)
        ), 503


@app.get("/tasks")
def get_tasks():

    with get_connection() as connection:

        with connection.cursor() as cursor:

            cursor.execute("""
                SELECT id, title, completed
                FROM tasks
                ORDER BY id
            """)

            rows = cursor.fetchall()

    tasks = [
        {
            "id": row[0],
            "title": row[1],
            "completed": row[2]
        }
        for row in rows
    ]

    return jsonify(tasks)


@app.post("/tasks")
def create_task():

    payload = request.get_json(silent=True) or {}

    title = payload.get("title")

    if not title:

        return jsonify(
            error="title is required"
        ), 400

    with get_connection() as connection:

        with connection.cursor() as cursor:

            cursor.execute("""
                INSERT INTO tasks (title)
                VALUES (%s)
                RETURNING id, title, completed
            """, (title,))

            row = cursor.fetchone()

    return jsonify(
        id=row[0],
        title=row[1],
        completed=row[2]
    ), 201