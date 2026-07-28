from datetime import date, timedelta


def _make_project(client):
    return client.post("/api/projects", json={"name": "P", "code": "P1"}).json()["id"]


def test_create_and_list_milestone(client):
    pid = _make_project(client)
    resp = client.post(
        f"/api/projects/{pid}/milestones", json={"name": "M1", "due_date": "2026-01-01"}
    )
    assert resp.status_code == 201
    assert resp.json()["status"] == "not_started"

    resp = client.get(f"/api/projects/{pid}/milestones")
    assert len(resp.json()) == 1


def test_overdue_flag_depends_on_due_date_and_status(client):
    pid = _make_project(client)
    past = (date.today() - timedelta(days=5)).isoformat()

    late = client.post(
        f"/api/projects/{pid}/milestones",
        json={"name": "Late", "due_date": past, "status": "not_started"},
    ).json()
    assert late["is_overdue"] is True

    done = client.post(
        f"/api/projects/{pid}/milestones",
        json={"name": "Done", "due_date": past, "status": "complete"},
    ).json()
    assert done["is_overdue"] is False

    future = client.post(
        f"/api/projects/{pid}/milestones",
        json={"name": "Future", "due_date": "2099-01-01", "status": "not_started"},
    ).json()
    assert future["is_overdue"] is False


def test_update_and_delete_milestone(client):
    pid = _make_project(client)
    mid = client.post(f"/api/projects/{pid}/milestones", json={"name": "M1"}).json()["id"]

    resp = client.put(f"/api/milestones/{mid}", json={"status": "complete"})
    assert resp.json()["status"] == "complete"

    resp = client.delete(f"/api/milestones/{mid}")
    assert resp.status_code == 204
    assert client.get(f"/api/projects/{pid}/milestones").json() == []


def test_milestones_for_missing_project_404(client):
    assert client.get("/api/projects/9999/milestones").status_code == 404
    assert client.post("/api/projects/9999/milestones", json={"name": "x"}).status_code == 404


def test_update_delete_missing_milestone_404(client):
    assert client.put("/api/milestones/9999", json={"status": "complete"}).status_code == 404
    assert client.delete("/api/milestones/9999").status_code == 404
