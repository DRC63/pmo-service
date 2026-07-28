def _project(client):
    return client.post("/api/projects", json={"name": "P", "code": "P1"}).json()["id"]


def test_create_risk_computes_score(client):
    pid = _project(client)
    resp = client.post(
        "/api/risks", json={"project_id": pid, "title": "R1", "likelihood": 4, "impact": 5}
    )
    assert resp.status_code == 201
    assert resp.json()["score"] == 20


def test_update_risk_recomputes_score_when_likelihood_or_impact_change(client):
    pid = _project(client)
    rid = client.post(
        "/api/risks", json={"project_id": pid, "title": "R1", "likelihood": 2, "impact": 2}
    ).json()["id"]

    resp = client.put(f"/api/risks/{rid}", json={"impact": 5})
    assert resp.json()["score"] == 10  # 2 * 5


def test_update_risk_without_score_fields_leaves_score_untouched(client):
    pid = _project(client)
    rid = client.post(
        "/api/risks", json={"project_id": pid, "title": "R1", "likelihood": 3, "impact": 3}
    ).json()["id"]

    resp = client.put(f"/api/risks/{rid}", json={"status": "closed"})
    assert resp.json()["score"] == 9
    assert resp.json()["status"] == "closed"


def test_list_risks_filters(client):
    pid = _project(client)
    client.post(
        "/api/risks", json={"project_id": pid, "title": "Low", "likelihood": 1, "impact": 1}
    )
    client.post(
        "/api/risks", json={"project_id": pid, "title": "High", "likelihood": 5, "impact": 5}
    )

    resp = client.get("/api/risks", params={"min_score": 15})
    assert [r["title"] for r in resp.json()] == ["High"]

    resp = client.get("/api/risks", params={"project_id": pid})
    assert len(resp.json()) == 2

    resp = client.get("/api/risks", params={"status": "closed"})
    assert resp.json() == []


def test_risk_requires_existing_project(client):
    resp = client.post(
        "/api/risks", json={"project_id": 9999, "title": "x", "likelihood": 1, "impact": 1}
    )
    assert resp.status_code == 404


def test_missing_risk_404s(client):
    assert client.get("/api/risks/9999").status_code == 404
    assert client.put("/api/risks/9999", json={"status": "closed"}).status_code == 404
    assert client.delete("/api/risks/9999").status_code == 404
