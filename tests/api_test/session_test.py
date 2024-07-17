def test_access_session(auth):
    print(auth)
    # with client:
    # data = {
    # "email": "selobu@gmail.com",
    # "password": "123456789"
    # }
    # response = client.post("/api/login/", json=data)
    # session is still accessible
    # response.json['fresh_access_token']
    # response.json['access_token']
    assert auth
