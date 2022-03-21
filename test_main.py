import os
import json

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

samples = {
    "added_to_space.json",
    "dialog_request.json",
    "removed_from_space.json",
    "slash_command_1.json",
    "text_message.json"
}

def from_json(fp: str) -> dict:
    with open(f"chat/samples/{fp}") as src:
        return json.load(src)

def test_added_to_space_route():
    sample = from_json("added_to_space.json")
    response = client.post("/", json=sample)
    print(response.json())
    assert response.status_code == 200

def test_text_message_route():
    sample = from_json("text_message.json")
    response = client.post("/", json=sample)
    print(response.json())
    assert response.status_code == 200

def test_removed_from_space_route():
    sample = from_json("removed_from_space.json")
    response = client.post("/", json=sample)
    print(response.json())
    assert response.status_code == 200

def test_slash_command_1_route():
    sample = from_json("slash_command_1.json")
    response = client.post("/", json=sample)
    print(response.json())
    assert response.status_code == 200

# def test_slash_command_2_route():
#     sample = from_json("slash_command_2.json")
#     response = client.post("/", json=sample)
#     print(response.json())
#     assert response.status_code == 200

def test_slash_command_3_route():
    sample = from_json("slash_command_3.json")
    response = client.post("/", json=sample)
    print(response.json())
    assert response.status_code == 200

def test_dialog_request_route():
    sample = from_json("dialog_request.json")
    response = client.post("/", json=sample)
    print(json.dumps(response.json(), indent=2))
    assert response.status_code == 200
