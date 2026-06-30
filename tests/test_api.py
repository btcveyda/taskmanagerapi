from fastapi.testclient import TestClient

from app.main import app, reset_store


client = TestClient(app)


def setup_function() -> None:
    reset_store()


def test_create_and_list_tasks() -> None:
    response = client.post(
        "/tasks",
        json={"title": "Write report", "description": "Finish by noon"},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Write report"
    assert body["description"] == "Finish by noon"
    assert body["status"] == "pending"

    list_response = client.get("/tasks")
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1


def test_filter_tasks_by_status() -> None:
    client.post("/tasks", json={"title": "First task"})
    client.post("/tasks", json={"title": "Second task", "status": "done"})

    response = client.get("/tasks", params={"status": "done"})

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Second task"


def test_update_and_delete_task() -> None:
    create_response = client.post("/tasks", json={"title": "Initial task"})
    task_id = create_response.json()["id"]

    update_response = client.put(
        f"/tasks/{task_id}",
        json={"status": "done", "title": "Updated task"},
    )
    assert update_response.status_code == 200
    assert update_response.json()["status"] == "done"

    delete_response = client.delete(f"/tasks/{task_id}")
    assert delete_response.status_code == 204

    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404


def test_validation_errors_are_422() -> None:
    response = client.post("/tasks", json={"title": 4, "status": "in_progress"})

    assert response.status_code == 422
    assert "title" in response.text
    assert "status" in response.text
