from conftest import make_token


def test_healthz_ohne_anmeldung(client):
    assert client.get("/healthz").status_code == 200


def test_ohne_anmeldung_401(client):
    response = client.get("/", headers={"Accept": "text/html"})
    assert response.status_code == 401
    assert "Anmeldung fehlt" in response.text
    assert "set-cookie" not in response.headers


def test_ungueltige_anmeldung_401(client):
    response = client.get("/", headers={"X-Portal-Assertion": make_token(aud=["andere-app"])})
    assert response.status_code == 401
    assert response.headers["content-type"] == "application/problem+json"


def test_keine_api_doku(client, as_student):
    for path in ("/docs", "/redoc", "/openapi.json"):
        assert client.get(path, headers=as_student).status_code == 404


def test_startseite(client):
    response = client.get("/", headers={"X-Portal-Assertion": make_token(roles=["employee"]), "Accept": "text/html"})
    assert response.status_code == 200
    html = response.text
    assert '<html lang="de">' in html
    assert 'href="#main"' in html
    assert html.count("<h1") == 1
    assert "set-cookie" not in response.headers


def test_urlaubstage_nur_eigene(client):
    kopf = {"X-Portal-Assertion": make_token(sub="student-test", roles=["employee"]), "Accept": "text/html"}
    response = client.get("/", headers=kopf)
    assert response.status_code == 200
    html = response.text
    assert "Weihnachtsurlaub" in html
    assert "23.12.2026" in html
    assert "Umzug" not in html  # Urlaubstag einer anderen Person
    assert '<th scope="col">Datum</th>' in html
    assert "<caption" in html
    assert html.count("<h1") == 1


def test_urlaubstage_ohne_eintraege(client):
    kopf = {"X-Portal-Assertion": make_token(sub="unbekannt", roles=["employee"]), "Accept": "text/html"}
    response = client.get("/", headers=kopf)
    assert response.status_code == 200
    assert "keine Urlaubstage eingetragen" in response.text


def test_urlaubstage_nicht_fuer_studierende(client, as_student):
    assert client.get("/", headers=as_student).status_code == 403
