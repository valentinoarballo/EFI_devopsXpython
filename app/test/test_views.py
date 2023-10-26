import pytest

from app import app, db
from app.models.models import Usuario


@pytest.fixture
def cliente():
    with app.app_context():
        db.create_all()
    
    cliente = app.test_client()

    yield cliente

    with app.app_context():
        db.session.rollback()
        # db.session.drop_all()


def test_get_all_users_fail(cliente):
    response = cliente.get('api/v1/user')

    # import ipdb; ipdb.set_trace()

    assert response.status_code == 404


def test_get_all_users(cliente):
    response = cliente.get('/user')

    # import ipdb; ipdb.set_trace()

    data = response.json
    assert response.status_code == 200


def test_create_user(cliente):
    data = dict(nombre="pkieeeeeeeeeeeeppito", email="pichicho3001", password="toilet")
    response = cliente.post("/user", json=data)
    
    # import ipdb; ipdb.set_trace()

    assert response.status_code == 201
