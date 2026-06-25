
async def test_register(client):
    response=await client.post("/auth/register",json={
        "username":"User1",
        "password":"12345"
    })
    assert response.status_code==201

async def test_register_same_username(client):
    data={
        "username":'User1',
        "password":"12345"
    }
    await client.post("/auth/register",json=data)
    response=await client.post("/auth/register",json=data)
    message=response.json()

    assert response.status_code==400
    assert message["detail"]=="this username already taken"

async def test_register_short_username(client):
    data={
        "username":"User",
        "password":"12345"
    }
    
    response=await client.post("/auth/register",json=data)
    message=(response.json())["detail"]

    assert response.status_code==422
    assert message[0]["msg"]=="Value error, Username must be between 5 and 12 characters"

async def test_register_short_password(client):
    data={
        "username":"User1",
        "password":"1234"
    }
    response=await client.post("/auth/register",json=data)
    message=(response.json())["detail"]

    assert response.status_code==422
    assert message[0]["msg"]=="Value error, Password must be between 5 and 12 characters"

async def test_register_long_username(client):
    data={
        "username":"this is long username test",
        "password":"12345"
    }

    response=await client.post("/auth/register",json=data)
    message=(response.json())["detail"]

    assert response.status_code==422
    assert message[0]["msg"]=="Value error, Username must be between 5 and 12 characters"

async def test_register_long_password(client):
    data={
        "username":"User1",
        "password":"this is long password test"
    }
    response=await client.post("/auth/register",json=data)
    message=(response.json())["detail"]

    assert response.status_code==422
    assert message[0]["msg"]=="Value error, Password must be between 5 and 12 characters"

async def test_login(client):
    await client.post("/auth/register",json={
        "username":"User1",
        "password":"12345"
    })
    response=await client.post("/auth/login",data={
        "username":"User1",
        "password":"12345"
    })
    assert response.status_code==200
    assert "access_token" in response.json()

async def test_login_wrong_password(registered_client,client):
    data={
        "username":"User1",
        "password":"wrong_password"
    }
    response=await client.post("auth/login",data=data)
    message=response.json()

    assert response.status_code==400
    assert message["detail"]=="username or password incorrect"