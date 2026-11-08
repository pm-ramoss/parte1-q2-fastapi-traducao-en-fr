from fastapi.testclient import TestClient

from app import main


def fake_translator(sentences, **kwargs):
    return [{"translation_text": f"[FR] {s}"} for s in sentences]


def test_translate_short_and_long_text():
    with TestClient(main.app) as client:
        main.resources["translator"] = fake_translator
        r1 = client.post("/translate", json={"text": "Hello."})
        r2 = client.post("/translate", json={"text": "Hello. How are you? Fine!"})
    assert r1.status_code == 200
    assert r1.json()["translated_text"] == "[FR] Hello."
    assert r2.json()["translated_text"] == "[FR] Hello. [FR] How are you? [FR] Fine!"


def test_empty_text_rejected():
    with TestClient(main.app) as client:
        r = client.post("/translate", json={"text": ""})
    assert r.status_code == 422
