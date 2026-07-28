def test_create_and_get_project(client):
    resp = client.post("/api/projects", json={"name": "Test", "code": "T1"})
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Test"
    assert data["rag_status"] == "green"
    assert data["category"] == "other"

    project_id = data["id"]
    resp = client.get(f"/api/projects/{project_id}")
    assert resp.status_code == 200
    detail = resp.json()
    assert detail["milestones"] == []
    assert detail["risks"] == []
    assert detail["allocations"] == []


def test_list_projects_filters(client):
    client.post(
        "/api/projects",
        json={"name": "A", "code": "A1", "category": "banking", "rag_status": "red"},
    )
    client.post(
        "/api/projects",
        json={"name": "B", "code": "B1", "category": "other", "rag_status": "green"},
    )

    resp = client.get("/api/projects", params={"category": "banking"})
    assert [p["name"] for p in resp.json()] == ["A"]

    resp = client.get("/api/projects", params={"rag_status": "green"})
    assert [p["name"] for p in resp.json()] == ["B"]


def test_update_project(client):
    resp = client.post("/api/projects", json={"name": "A", "code": "A1"})
    pid = resp.json()["id"]

    resp = client.put(f"/api/projects/{pid}", json={"rag_status": "amber"})
    assert resp.status_code == 200
    assert resp.json()["rag_status"] == "amber"
    assert resp.json()["name"] == "A"  # untouched fields survive a partial update


def test_delete_project_cascades(client):
    resp = client.post("/api/projects", json={"name": "A", "code": "A1"})
    pid = resp.json()["id"]
    client.post(f"/api/projects/{pid}/milestones", json={"name": "M1"})
    client.post(
        "/api/risks",
        json={"project_id": pid, "title": "R1", "likelihood": 2, "impact": 2},
    )

    resp = client.delete(f"/api/projects/{pid}")
    assert resp.status_code == 204
    assert client.get(f"/api/projects/{pid}").status_code == 404


def test_missing_project_404s(client):
    assert client.get("/api/projects/9999").status_code == 404
    assert client.put("/api/projects/9999", json={"name": "x"}).status_code == 404
    assert client.delete("/api/projects/9999").status_code == 404
