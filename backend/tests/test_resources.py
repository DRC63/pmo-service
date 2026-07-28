def test_create_list_get_resource(client):
    resp = client.post("/api/resources", json={"name": "Alice", "role": "PM"})
    assert resp.status_code == 201
    rid = resp.json()["id"]

    resp = client.get("/api/resources")
    assert len(resp.json()) == 1

    resp = client.get(f"/api/resources/{rid}")
    assert resp.status_code == 200
    assert resp.json()["allocations"] == []


def test_active_filter(client):
    client.post("/api/resources", json={"name": "Active1", "active": True})
    client.post("/api/resources", json={"name": "Inactive1", "active": False})

    resp = client.get("/api/resources", params={"active": True})
    assert [r["name"] for r in resp.json()] == ["Active1"]

    resp = client.get("/api/resources", params={"active": False})
    assert [r["name"] for r in resp.json()] == ["Inactive1"]


def test_update_and_delete_resource(client):
    rid = client.post("/api/resources", json={"name": "Bob"}).json()["id"]

    resp = client.put(f"/api/resources/{rid}", json={"role": "BA"})
    assert resp.json()["role"] == "BA"
    assert resp.json()["name"] == "Bob"

    resp = client.delete(f"/api/resources/{rid}")
    assert resp.status_code == 204
    assert client.get(f"/api/resources/{rid}").status_code == 404


def test_missing_resource_404s(client):
    assert client.get("/api/resources/9999").status_code == 404
    assert client.put("/api/resources/9999", json={"name": "x"}).status_code == 404
    assert client.delete("/api/resources/9999").status_code == 404
