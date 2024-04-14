# import the fixtures (this is necessary!)
from ..fixtures import app, client, agency
import json

def test_get_newspaper_should_list_all_papers(client, agency):
    # send request
    response = client.get("/newspaper/")   # <-- note the slash at the end!

    # test status code
    assert response.status_code == 200

    # parse response and check that the correct data is here
    parsed = response.get_json()
    assert len(parsed["newspapers"]) == len(agency.newspapers)


def test_add_newspaper(client, agency):
    # prepare
    paper_count_before = len(agency.newspapers)

    # act
    response = client.post("/newspaper/",  # <-- note the slash at the end!
                           json={
                               "name": "Simpsons Comic",
                               "frequency": 7,
                               "price": 3.14
                           })
    assert response.status_code == 200
    # verify

    assert len(agency.newspapers) == paper_count_before + 1
    # parse response and check that the correct data is here
    parsed = response.get_json()

    # verify that the response contains the newspaper data
    assert parsed["name"] == "Simpsons Comic"
    assert parsed["frequency"] == 7
    assert parsed["price"] == 3.14

def test_get_newspaper(client, agency):
    for newspaper in agency.newspapers:
        response = client.get(f"/newspaper/{newspaper.paper_id}")
        parsed = response.get_json()
        assert response.status_code == 200
        assert parsed["name"] == newspaper.name
        assert parsed["frequency"] == newspaper.frequency
        assert parsed["price"] == newspaper.price

def test_get_invalid_newspaper(client):
    response = client.get(f"/newspaper/1001")
    assert response.status_code == 200
    parsed = response.get_json()
    assert parsed == "Newspaper with ID 1001 was not found"


def test_update_newspaper(client, agency):
        for newspaper in agency.newspapers:
            response = client.post(f"/newspaper/{newspaper.paper_id}",
                                json = {
                                    "name": "Simpsons Comic",
                                    "frequency": 7,
                                    "price": 3.14
                                })
            parsed = response.get_json()
            assert response.status_code == 200
            assert parsed["name"] == "Simpsons Comic"
            assert parsed["frequency"] == 7
            assert parsed["price"] == 3.14

def test_delete_newspaper(client, agency):
    for newspaper in agency.newspapers:
        before = len(agency.newspapers)
        response = client.delete(f"/newspaper/{newspaper.paper_id}")
        assert response.status_code == 200
        assert before == len(agency.newspapers) + 1

def delete_invalid_newspaper(client):
    response = client.delete("/newspaper/1001")
    assert response.status_code == 200
    parsed = response.get_json()
    assert parsed == "Newspaper with ID 1001 was not found"

def test_add_issue(client, agency):
    paper = agency.get_newspaper(100)
    before = len(paper.get_issues())
    response = client.post("/newspaper/100/issue",
                           json={
                               "name": "Test Issue",
                               "releasedate": "2022-01-01T00:00:00",
                               "released": True
                           })

    assert response.status_code == 200
    parsed = response.get_json()

    assert parsed["name"] == "Test Issue"
    assert parsed["releasedate"] == "2022-01-01T00:00:00"
    assert parsed["released"] == True
    
    assert len(paper.get_issues()) == before + 1
    assert paper.get_issues()[-1].name == "Test Issue"


def test_get_issues(client, agency):
    response = client.get("/newspaper/100/issue")
    parsed = response.get_json()
    assert response.status_code == 200
    assert len(parsed) == len(agency.get_newspaper(100).get_issues())
    assert parsed[0]["name"] == agency.get_newspaper(100).get_issues()[0].name
    assert parsed[1]["name"] == agency.get_newspaper(100).get_issues()[1].name

def test_get_issue(client, agency):
    response = client.get("/newspaper/100/issue/100")
    parsed = response.get_json()
    assert response.status_code == 200
    assert parsed["released"] == agency.get_newspaper(100).get_issue(100).released
    assert parsed["name"] == agency.get_newspaper(100).get_issue(100).name
    assert parsed["releasedate"] == agency.get_newspaper(100).get_issue(100).releasedate

def test_get_invalid_issue(client):
    response = client.get("/newspaper/100/issue/1001")
    assert response.status_code == 200
    parsed = response.get_json()
    assert parsed == "Issue with ID 1001 was not found"

def test_release_issue(client, agency):
    before_released = agency.get_newspaper(100).get_issue(102).released
    client.post("/newspaper/100/issue/102/release")
    updated_released = agency.get_newspaper(100).get_issue(102).released
    assert before_released != updated_released

def test_set_issue_editor(client, agency):
    response = client.post("/newspaper/100/issue/100/editor?editor_id=100")

    assert response.status_code == 200
    parsed = response.get_json()
    assert parsed == "Editor with ID 100 work on Vol. 1"
    assert agency.get_newspaper(100).get_issue(100).editor_id == 100


def test_send_issue(client, agency):
    response = client.post("/newspaper/100/issue/100/deliver?subscriber_id=100")
    assert response.status_code == 200
    parsed = response.get_json()
    assert parsed == "Issue was sent to a subscriber with ID 100"
    issue = agency.get_newspaper(100).get_issue(100)
    subscriber = agency.get_subscriber(100)
    assert subscriber in issue.send_to






