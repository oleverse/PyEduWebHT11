from unittest.mock import MagicMock, patch

import pytest

from api.database.models import User
from api.services.auth import auth_service


@pytest.fixture()
def token(client, user, session, monkeypatch):
    mock_send_email = MagicMock()
    monkeypatch.setattr("api.routes.auth.send_email", mock_send_email)
    client.post("/api/auth/register", json=user)
    current_user: User = session.query(User).filter(User.email == user.get('email')).first()
    current_user.confirmed = True
    session.commit()
    response = client.post(
        "/api/auth/login",
        data={"username": user.get('email'), "password": user.get('password')},
    )
    data = response.json()
    return data["access_token"]


def is_valid_result(result):
    return all([
        lambda k, v: k == v for k, v in [
            (result["first_name"], "first"),
            (result["last_name"], "last"),
            (result["email"], "contact@example.com"),
            (result["phone"], "677692840236"),
            (result["birth_date"], "1994-07-14"),
            (result["description"], "descr")
        ]
    ])


def test_create_contact(client, token):
    with patch.object(auth_service, 'redis_data') as r_mock:
        r_mock.get.return_value = None
        response = client.post(
            "/api/contacts",
            json={
                "first_name": "first",
                "last_name": "last",
                "email": "contact@example.com",
                "phone": "677692840236",
                "birth_date": "1994-07-14",
                "description": "descr"
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 201, response.text
        data = response.json()
        assert is_valid_result(data)
        assert "id" in data


def test_get_contact(client, token):
    with patch.object(auth_service, 'redis_data') as r_mock:
        r_mock.get.return_value = None
        response = client.get(
            "/api/contacts/1",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert is_valid_result(data)
        assert "id" in data


def test_get_contact_not_found(client, token):
    with patch.object(auth_service, 'redis_data') as r_mock:
        r_mock.get.return_value = None
        response = client.get(
            "/api/contacts/2",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == "Contact not found"


def test_get_contacts(client, token):
    with patch.object(auth_service, 'redis_data') as r_mock:
        r_mock.get.return_value = None
        response = client.get(
            "/api/contacts",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert isinstance(data, list)
        assert is_valid_result(data[0])
        assert "id" in data[0]


def test_update_contact(client, token):
    with patch.object(auth_service, 'redis_data') as r_mock:
        r_mock.get.return_value = None
        response = client.put(
            "/api/contacts/1",
            json={"name": "new_test_tag"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert is_valid_result(data)
        assert "id" in data


def test_update_contact_not_found(client, token):
    with patch.object(auth_service, 'redis_data') as r_mock:
        r_mock.get.return_value = None
        response = client.put(
            "/api/contacts/2",
            json={"name": "new_test_tag"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == "Contact not found"


def test_delete_contact(client, token):
    with patch.object(auth_service, 'redis_data') as r_mock:
        r_mock.get.return_value = None
        response = client.delete(
            "/api/contacts/1",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert is_valid_result(data)
        assert "id" in data


def test_repeat_delete_contact(client, token):
    with patch.object(auth_service, 'redis_data') as r_mock:
        r_mock.get.return_value = None
        response = client.delete(
            "/api/contacts/1",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 404, response.text
        data = response.json()
        assert data["detail"] == "Contact not found"
