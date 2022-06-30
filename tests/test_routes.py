from fastapi.testclient import TestClient
from cocktail_api.main import app

client = TestClient(app)

def test_index():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message":"welcome to the cocktail-api!"}