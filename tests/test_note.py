async def test_creaate_note(registered_client):
    response= await registered_client.post("/notes/",json={
        "head":"test1",
        "content":"this is test"
    })

    data=response.json()
    assert data["head"]=="test1"
    assert data["content"]=="this is test"
    assert response.status_code == 200

async def test_create_short_head(registered_client):
    data={
        "head":"test",
        "content":"this is test"
    }
    response=await registered_client.post("notes/",json=data)
    message=(response.json())["detail"]

    assert message[0]["msg"]=="Value error, Head must be between 5 and 20 characters"
    assert response.status_code==422

async def test_create_short_content(registered_client):
    data={
        "head":"test1",
        "content":"test"
    }
    response=await registered_client.post("notes/",json=data)
    message=(response.json())["detail"]

    assert message[0]["msg"]=="Value error, Content must be between 10 and 100 characters"
    assert response.status_code==422

async def test_create_long_head(registered_client):
    data={
        "head":"this is for long head test",
        "content":"this is test"
    }
    response=await registered_client.post("notes/",json=data)
    message=(response.json())["detail"]

    assert message[0]["msg"]=="Value error, Head must be between 5 and 20 characters"
    assert response.status_code==422

async def test_create_long_content(registered_client):
    data={
        "head":"test1",
        "content":"This is a test sentence that is specifically designed to be longer than one hundred characters in total length."
    }
    response=await registered_client.post("notes/",json=data)
    message=(response.json())["detail"]

    assert message[0]["msg"]=="Value error, Content must be between 10 and 100 characters"
    assert response.status_code==422

async def test_create_note_not_authorized(client):
    data={
        "head":"test1",
        "content":"this is test"
    }
    response=await client.post("/notes/",json=data)
    message=response.json()

    assert response.status_code==401
    assert message["detail"]=="Not authenticated"

async def test_update_note_content(created_note,registered_client):
    data={
        "content":"this is test"
    }
    id=created_note["id"]
    response=await registered_client.put(f"/notes/{id}",json=data)
    assert (response.json())["content"]=="this is test"
    assert response.status_code==200

async def test_update_note_head(created_note,registered_client):
    data={
        "head":"this is updated test"
    }
    id=created_note["id"]
    response=await registered_client.put(f"/notes/{id}",json=data)
    assert (response.json())["head"]=="this is updated test"
    assert response.status_code==200

async def test_delete_note(created_note,registered_client):
    id=created_note["id"]
    response= await registered_client.delete(f"/notes/{id}")
    message=response.json()
    assert response.status_code==200
    assert message["status"]=="success"
    assert message["message"]=="successfuly deleted"

async def test_forbidden_delete_note(created_note,client):
    data={
        "username":"tamerlan",
        "password":"12345S"
    }
    id=created_note["id"]
    await client.post("/auth/register",json=data)
    login=await client.post("/auth/login",data=data)
    token=(login.json())["access_token"]
    client.headers.update({"Authorization":f"Bearer {token}"})
    response=await client.delete(f"/notes/{id}")
    message=response.json()
    
    assert response.status_code==403
    assert message["detail"]=="Forbidden"

async def test_get_all_notes(created_note,client):
    response=await client.get("/notes/")
    message=(response.json())[0]
    assert response.status_code==200
    assert message["head"]=="test1"
    assert message["content"]=="this is test"

async def test_note_get_by_id(created_note,client):
    id=created_note["id"]
    response=await client.get(f"notes/{id}")
    message=response.json()
    assert response.status_code==200
    assert message["head"]=="test1"
    assert message["content"]=="this is test"

async def test_not_found_note_get_by_id(client):
    response=await client.get("notes/5")
    message=response.json()
    assert response.status_code==404
    assert message["detail"]=="Note not Found"