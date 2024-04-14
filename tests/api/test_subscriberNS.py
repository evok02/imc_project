from ..fixtures import app, client, agency


def test_get_subscribers(agency, client):
    response = client.get("/subscriber/")
    assert response.status_code == 200
    parsed = response.get_json()
    assert len(parsed["subscribers"]) == len(agency.get_subscribers())

def test_add_subscriber(agency, client):
    before = len(agency.get_subscribers())
    response = client.post("/subscriber/", json = {
        "name":"Hlib Tereshchenko"
    })
    assert response.status_code == 200
    parsed = response.get_json()
    assert parsed["subscriber"]["name"] == "Hlib Tereshchenko"
    assert before == len(agency.get_subscribers()) - 1

def test_get_subscriber(agency, client):
    for subscriber in agency.get_subscribers():
        response = client.get(f"/subscriber/{subscriber.id}")
        assert response.status_code == 200
        parsed = response.get_json()
        assert parsed["id"] == subscriber.id
        assert parsed["name"] == subscriber.name

def test_get_invalid_subscriber(client):
    response = client.get("/subscriber/1001")
    assert response.status_code == 200
    parsed = response.get_json()
    assert parsed == "Subscriber with ID 1001 was not found"

def test_subscriber_subscribe(agency, client):
    for subscriber in agency.subscribers:
        response = client.post(f"/subscriber/{subscriber.id}/subscribe?paper_id=100")
        assert response.status_code == 200
        parsed = response.get_json()
        assert parsed == f"Subscriber was subscribed to a newspaper with ID 100"

def test_subscriber_stats(client, agency):
    subscriber = agency.subscribers[0]
    newspaper = agency.newspapers[0]
    subscriber.subscribe(newspaper)
    for issue in newspaper.issues:
        issue.send_issue(subscriber)
    response = client.get(f"/subscriber/{subscriber.id}/stats")
    assert response.status_code == 200
    stats = response.get_json()
    assert stats["Number of subscribed newspapers"] == len(subscriber.subscribed_newspapers)
    assert stats["Monthly cost"] == sum(paper.price for paper in subscriber.subscribed_newspapers)
    assert stats["Annual cost"] == 12 * sum(paper.price for paper in subscriber.subscribed_newspapers)





    