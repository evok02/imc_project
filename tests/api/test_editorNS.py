from ..fixtures import app, client, agency

def test_get_editors(agency, client):
    response = client.get("/editor/")
    assert response.status_code == 200
    parsed = response.get_json()
    assert len(parsed["editor"]) == len(agency.editors)

def test_add_editor(agency, client):
    before = len(agency.get_editors())
    response = client.post("/editor/", json = {
        "name": "Mark Twain"
    })
    assert response.status_code == 200
    assert before == len(agency.get_editors()) - 1

def test_get_editor(agency, client):
    response = client.get("/editor/100")
    assert response.status_code == 200
    parsed = response.get_json()
    editor = agency.get_editor(100)
    assert parsed["name"] == editor.name
    assert parsed["id"] == editor.id

def test_get_invalid_editor(client):
    response = client.get("/editor/1001")
    assert response.status_code == 200
    parsed = response.get_json()
    assert parsed == "Editor with ID 1001 was not found"

def test_update_editor(agency, client):
    response = client.post("/editor/101", json = {
        "name":"Mark Twain"
    })
    assert response.status_code == 200
    parsed = response.get_json()
    assert parsed["name"] == "Mark Twain"

def test_delete_editor(agency, client):
    for editor in agency.editors:
        before = len(agency.editors)
        response = client.delete(f"/editor/{editor.id}")
        assert response.status_code == 200
        parsed = response.get_json()
        assert parsed == f"Editor with ID {editor.id} was deleted"
        assert len(agency.editors) == before - 1

def test_delete_invalid_editor(client):
    response = client.delete("/editor/1001")
    assert response.status_code == 200
    parsed = response.get_json()
    assert parsed == "Editor with ID 1001 was not found"

def test_get_editor_issues(agency, client):
    editor = agency.get_editor(100)
    agency.get_newspaper(100).get_issue(100).set_editor(editor)
    agency.get_newspaper(101).get_issue(100).set_editor(editor)
    agency.get_newspaper(115).get_issue(100).set_editor(editor)
    response = client.get("editor/100/issues")
    assert response.status_code == 200
    parsed = response.get_json()
    assert len(parsed) == len(agency.get_editor(100).work_on_issues)



    




    