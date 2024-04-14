import pytest

from ...src.model.newspaper import Newspaper
from ...src.model.agency import Agency
from ...src.model.editor import Editor
from ...src.model.subscriber import Subscriber
from ..fixtures import app, client, agency
from ..testdata import populate


def test_add_newspaper(agency):
    before = len(agency.newspapers)
    new_paper = Newspaper(paper_id=999,
                          name="Simpsons Comic",
                          frequency=7,
                          price=3.14)
    agency.add_newspaper(new_paper)
    assert len(agency.all_newspapers()) == before + 1


def test_add_newspaper_same_id_should_raise_error():
    agency = Agency()
    before = len(agency.newspapers)
    new_paper = Newspaper(paper_id=999,
                          name="Simpsons Comic",
                          frequency=7,
                          price=3.14)

    # first adding of newspaper should be okay
    agency.add_newspaper(new_paper)

    new_paper2 = Newspaper(paper_id=999,
                          name="Superman Comic",
                          frequency=7,
                          price=13.14)

    with pytest.raises(ValueError, match='A newspaper with ID 999 already exists'):  # <-- this allows us to test for exceptions
        # this one should rais ean exception!
        agency.add_newspaper(new_paper2)


def test_get_newspaper(agency):
    result1 = agency.get_newspaper(100)
    result2 = agency.get_newspaper(101)
    result3 = agency.get_newspaper(0)
    assert (result1.paper_id == 100)
    assert (result2.paper_id == 101)
    assert (result3 == None)

def test_all_newspapers(agency):
    result = agency.all_newspapers()
    assert len(result) == len(agency.newspapers)

def test_remove_newspaper(agency):
    new_paper = Newspaper(paper_id=9897988,
                          name="Reuters",
                          frequency=7,
                          price=3.14)
    agency.newspapers.append(new_paper)
    before = len(agency.newspapers)
    agency.remove_newspaper(new_paper)
    after = len(agency.newspapers)
    assert(before == after + 1)

def test_get_editors(agency):
    result = agency.get_editors()
    assert len(agency.editors) == len(result)

def test_get_editor(agency):
    result1 = agency.get_editor(100)
    result2 = agency.get_editor(101)
    result3 = agency.get_editor(102)
    result4 = agency.get_editor(0)
    assert (result1.id == 100)
    assert (result2.id == 101)
    assert (result3.id == 102)
    assert (result4 == None)

def test_add_editor(agency):
    before = len(agency.editors)
    new_editor = Editor(id=999,
                        name="Tom Clancy")
    agency.add_editor(new_editor)
    after = len(agency.editors)
    assert before == after - 1

def test_add_editor_same_id_should_raise_error(agency):
    new_editor = Editor(id=888,
                        name="Tom Clancy")
    agency.add_editor(new_editor)
    new_editor2 = Editor(id=888,
                        name="Tom Clancy")
    with pytest.raises(ValueError, match="An editor with ID 888 already exists"):
        agency.add_editor(new_editor2)

def test_get_subscribers(agency):
    result = agency.get_subscribers()
    assert (len(result)==len(agency.subscribers))

def test_add_subscriber(agency):
    before = len(agency.subscribers)
    new_subscriber= Subscriber(id=999,
                        name="Hlib Tereshchenko")
    agency.add_subscriber(new_subscriber)
    after = len(agency.subscribers)
    assert before == after - 1

def test_add_subscriber_same_id_should_raise_error(agency):
    new_subscriber1 = Subscriber(id=888,
                                 name = "Hlib Tereshchenko")
    agency.add_subscriber(new_subscriber1)
    new_subscriber2 = Subscriber(id=888,
                                 name="Hlib Tereshchenko")
    with pytest.raises(ValueError, match="A subscriber with ID 888 already exists"):
        agency.add_subscriber(new_subscriber2)


def test_get_subscriber(agency):
    result1 = agency.get_subscriber(100)
    result2 = agency.get_subscriber(101)
    result3 = agency.get_subscriber(102)
    result4 = agency.get_editor(0)
    assert (result1.id == 100)
    assert (result2.id == 101)
    assert (result3.id == 102)
    assert (result4 == None)

def test_remove_subscriber(agency):
    new_subscriber = Subscriber(id=9897988,
                          name="Arsenii Kobelyanskii")
    agency.subscribers.append(new_subscriber)
    before = len(agency.subscribers)
    agency.remove_subscriber(new_subscriber)
    after = len(agency.subscribers)
    assert(before == after + 1)

