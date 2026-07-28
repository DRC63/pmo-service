def test_portfolio_report_rollup(client):
    pid = client.post(
        "/api/projects", json={"name": "A", "code": "A1", "budget": 1000, "actual_spend": 200}
    ).json()["id"]
    client.post(f"/api/projects/{pid}/milestones", json={"name": "M1", "status": "complete"})
    client.post(f"/api/projects/{pid}/milestones", json={"name": "M2", "status": "not_started"})
    client.post(
        "/api/risks", json={"project_id": pid, "title": "R1", "likelihood": 5, "impact": 5}
    )

    resp = client.get("/api/reports/portfolio")
    assert resp.status_code == 200
    row = resp.json()[0]
    assert row["pct_milestones_complete"] == 50.0
    assert row["open_risk_count"] == 1
    assert row["top_risk_score"] == 25
    assert row["budget"] == 1000
    assert row["actual_spend"] == 200


def test_portfolio_report_excludes_closed_risks_from_open_count(client):
    pid = client.post("/api/projects", json={"name": "A", "code": "A1"}).json()["id"]
    rid = client.post(
        "/api/risks", json={"project_id": pid, "title": "R1", "likelihood": 3, "impact": 3}
    ).json()["id"]
    client.put(f"/api/risks/{rid}", json={"status": "closed"})

    resp = client.get("/api/reports/portfolio")
    row = resp.json()[0]
    assert row["open_risk_count"] == 0
    assert row["top_risk_score"] == 0


def test_project_report(client):
    pid = client.post("/api/projects", json={"name": "A", "code": "A1"}).json()["id"]
    resp = client.get(f"/api/reports/project/{pid}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["project"]["name"] == "A"
    assert data["pct_milestones_complete"] == 0


def test_project_report_missing_project_404(client):
    assert client.get("/api/reports/project/9999").status_code == 404
