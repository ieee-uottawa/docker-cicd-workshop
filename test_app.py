import app


def test_home_endpoint():
    client = app.app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert response.get_json() == {"message": "Docker + CI/CD workshop server"}


def test_health_endpoint():
    client = app.app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_config_endpoint_default_values(monkeypatch):
    monkeypatch.delenv("APP_MESSAGE", raising=False)
    monkeypatch.delenv("IPIFY_URL", raising=False)
    monkeypatch.delenv("DEMO_SECRET_FILE", raising=False)

    client = app.app.test_client()
    response = client.get("/config")

    assert response.status_code == 200
    body = response.get_json()
    assert body["app_message"] == "Docker + CI/CD workshop server"
    assert body["ipify_url"] == "https://api.ipify.org?format=json"
    assert body["has_demo_secret"] is False


def test_ip_endpoint_success(monkeypatch):
    def mock_get_ip():
        return "203.0.113.10", None

    monkeypatch.setattr(app, "get_ip", mock_get_ip)
    client = app.app.test_client()

    response = client.get("/ip")

    assert response.status_code == 200
    assert response.get_json() == {"ip": "203.0.113.10"}


def test_ip_endpoint_error(monkeypatch):
    def mock_get_ip():
        return None, "network down"

    monkeypatch.setattr(app, "get_ip", mock_get_ip)
    client = app.app.test_client()

    response = client.get("/ip")

    assert response.status_code == 502
    assert response.get_json() == {"error": "network down"}


def test_add_endpoint_success():
    client = app.app.test_client()

    response = client.get("/add?a=2&b=3")

    assert response.status_code == 200
    assert response.get_json() == {"result": 5}


def test_add_endpoint_invalid_params():
    client = app.app.test_client()

    response = client.get("/add?a=x&b=3")

    assert response.status_code == 400
    assert response.get_json() == {"error": "Params a and b must be integers"}


def test_add_function():
    assert app.add(2, 3) == 5
    assert app.add(-1, 1) == 0
    assert app.add(0, 0) == 0
