import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# Ensure src is importable
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from app import app, activities  # noqa: E402

client = TestClient(app)


def test_signup_and_delete_flow():
    activity = "Chess Club"
    email = "test@example.com"

    # Ensure the participant is not present before test
    if email in activities[activity]["participants"]:
        activities[activity]["participants"] = [p for p in activities[activity]["participants"] if p != email]

    # Signup successful
    r = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert r.status_code == 200
    assert f"Signed up {email}" in r.json().get("message", "")

    # Duplicate signup should return 400
    r2 = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert r2.status_code == 400

    # Delete participant
    r3 = client.delete(f"/activities/{activity}/participants", params={"email": email})
    assert r3.status_code == 200

    # Deleting again should return 404
    r4 = client.delete(f"/activities/{activity}/participants", params={"email": email})
    assert r4.status_code == 404
