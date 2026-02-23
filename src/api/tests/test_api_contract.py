import pytest
import requests

def test_user_contract_basic():
    res = requests.get("https://jsonplaceholder.typicode.com/users/1", timeout=20)
    assert res.status_code == 200

    body = res.json()
    assert "id" in body and isinstance(body["id"], int)
    assert "name" in body and isinstance(body["name"], str) and body["name"]
