def _setup(client):
    pid = client.post("/api/projects", json={"name": "P", "code": "P1"}).json()["id"]
    rid = client.post("/api/resources", json={"name": "R"}).json()["id"]
    return pid, rid


def test_create_and_list_allocation(client):
    pid, rid = _setup(client)
    resp = client.post(
        "/api/allocations",
        json={"resource_id": rid, "project_id": pid, "allocation_pct": 50},
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["resource_name"] == "R"
    assert body["project_name"] == "P"

    resp = client.get("/api/allocations", params={"resource_id": rid})
    assert len(resp.json()) == 1

    resp = client.get("/api/allocations", params={"project_id": pid})
    assert len(resp.json()) == 1


def test_allocation_requires_existing_resource_and_project(client):
    pid, rid = _setup(client)
    assert (
        client.post(
            "/api/allocations",
            json={"resource_id": 9999, "project_id": pid, "allocation_pct": 10},
        ).status_code
        == 404
    )
    assert (
        client.post(
            "/api/allocations",
            json={"resource_id": rid, "project_id": 9999, "allocation_pct": 10},
        ).status_code
        == 404
    )


def test_update_and_delete_allocation(client):
    pid, rid = _setup(client)
    aid = client.post(
        "/api/allocations",
        json={"resource_id": rid, "project_id": pid, "allocation_pct": 50},
    ).json()["id"]

    resp = client.put(f"/api/allocations/{aid}", json={"allocation_pct": 75})
    assert resp.json()["allocation_pct"] == 75

    resp = client.delete(f"/api/allocations/{aid}")
    assert resp.status_code == 204


def test_duplicate_resource_project_allocation_returns_409(client):
    pid, rid = _setup(client)
    payload = {"resource_id": rid, "project_id": pid, "allocation_pct": 50}
    assert client.post("/api/allocations", json=payload).status_code == 201

    resp = client.post("/api/allocations", json=payload)
    assert resp.status_code == 409
    assert "already allocated" in resp.json()["detail"]

    # the failed insert must not have left a duplicate row or a broken session
    resp = client.get("/api/allocations", params={"resource_id": rid, "project_id": pid})
    assert len(resp.json()) == 1
