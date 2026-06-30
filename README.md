# Task Manager API

A simple FastAPI-based REST API for managing daily tasks with CRUD operations, status filtering, and automatic OpenAPI/Swagger documentation.

## Features
- Create, read, update, and delete tasks
- Filter tasks by status with `pending` or `done`
- Strict Pydantic validation with clear 422 responses
- Interactive API docs at `/docs`

## Run locally

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the server:
   ```bash
   uvicorn app.main:app --reload
   ```
3. Open the interactive documentation:
   - http://127.0.0.1:8000/docs

## Example endpoints
- `GET /tasks`
- `GET /tasks/{task_id}`
- `POST /tasks`
- `PUT /tasks/{task_id}`
- `DELETE /tasks/{task_id}`

## Testing
```bash
pytest -q
```
