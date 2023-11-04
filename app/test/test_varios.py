import pytest
from app import app
from app.schemas import temaSchema


@pytest.fixture
def client():
    # Crea un cliente de prueba para tu aplicación Flask
    with app.test_client() as client:
        yield client


def test_agregar_tema(client):
    # Define el nombre del tema que quieres agregar
    nombre = "juegos"
    # Define el diccionario JSON que vas a enviar en el body de la request
    data = {"nombre": nombre}
    # Envía una petición POST al endpoint de temas con el diccionario JSON
    response = client.post("/temas", json=data)
    # Verifica que la respuesta tenga el código de estado 200 (OK)
    assert response.status_code == 200
    # Verifica que la respuesta tenga el tipo de contenido JSON
    assert response.content_type == "application/json"
    # Verifica que la respuesta tenga el campo "AGREGADO" con el nombre del tema
    assert response.json["AGREGADO"] == temaSchema().dump(data)

