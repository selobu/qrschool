def test_create_app(client):
    response = client.get("/api")
    assert b"http://localhost/api/" in response.data
