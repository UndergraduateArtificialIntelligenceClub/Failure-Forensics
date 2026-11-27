import pytest
from fastapi.testclient import TestClient

from app import main


def test_health_does_not_need_settings(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("POSTGRES_PORT", "invalid")

    with TestClient(main.app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.parametrize("failed_service", [None, "postgres", "redis", "minio"])
def test_ready(
    monkeypatch: pytest.MonkeyPatch,
    failed_service: str | None,
) -> None:
    checks = {
        "postgres": failed_service != "postgres",
        "redis": failed_service != "redis",
        "minio": failed_service != "minio",
    }
    monkeypatch.setenv("POSTGRES_PORT", "5432")
    monkeypatch.setattr(main, "check_postgres", lambda settings: checks["postgres"])
    monkeypatch.setattr(main, "check_redis", lambda settings: checks["redis"])
    monkeypatch.setattr(main, "check_minio", lambda settings: checks["minio"])

    with TestClient(main.app) as client:
        response = client.get("/ready")

    assert response.status_code == (200 if failed_service is None else 503)
    assert response.json() == {
        "status": "ready" if failed_service is None else "not_ready",
        "checks": checks,
    }
