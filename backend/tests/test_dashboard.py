from datetime import date, timedelta


def test_dashboard_summary_empty(client):
    resp = client.get("/api/dashboard/summary")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total_projects"] == 0
    assert data["rag_counts"] == {"green": 0, "amber": 0, "red": 0}
    assert data["upcoming_milestones"] == []
    assert data["high_severity_risks"] == []
    assert data["overdue_milestones_count"] == 0


def test_dashboard_summary_with_data(client):
    p1 = client.post(
        "/api/projects", json={"name": "A", "code": "A1", "rag_status": "red"}
    ).json()["id"]
    p2 = client.post(
        "/api/projects", json={"name": "B", "code": "B1", "rag_status": "green"}
    ).json()["id"]

    soon = (date.today() + timedelta(days=5)).isoformat()
    far = (date.today() + timedelta(days=60)).isoformat()
    past = (date.today() - timedelta(days=3)).isoformat()

    client.post(f"/api/projects/{p1}/milestones", json={"name": "Soon", "due_date": soon})
    client.post(f"/api/projects/{p1}/milestones", json={"name": "Far", "due_date": far})
    client.post(f"/api/projects/{p1}/milestones", json={"name": "Past", "due_date": past})

    client.post(  # score 25 -> high severity
        "/api/risks", json={"project_id": p1, "title": "Big", "likelihood": 5, "impact": 5}
    )
    client.post(  # score 1 -> not high severity
        "/api/risks", json={"project_id": p2, "title": "Small", "likelihood": 1, "impact": 1}
    )

    resp = client.get("/api/dashboard/summary")
    data = resp.json()

    assert data["total_projects"] == 2
    assert data["rag_counts"]["red"] == 1
    assert data["rag_counts"]["green"] == 1
    assert data["overdue_milestones_count"] == 1

    upcoming_names = {m["name"] for m in data["upcoming_milestones"]}
    assert upcoming_names == {"Soon"}  # Far is beyond 30d, Past is overdue not upcoming

    high_sev_titles = [r["title"] for r in data["high_severity_risks"]]
    assert high_sev_titles == ["Big"]


def test_closed_high_severity_risk_excluded_from_dashboard(client):
    pid = client.post("/api/projects", json={"name": "A", "code": "A1"}).json()["id"]
    rid = client.post(
        "/api/risks", json={"project_id": pid, "title": "Closed Big", "likelihood": 5, "impact": 5}
    ).json()["id"]
    client.put(f"/api/risks/{rid}", json={"status": "closed"})

    resp = client.get("/api/dashboard/summary")
    assert resp.json()["high_severity_risks"] == []
