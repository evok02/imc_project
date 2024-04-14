from ..src.model.agency import Agency
from ..src.model.newspaper import Newspaper
from ..src.model.editor import Editor
from ..src.model.subscriber import Subscriber
from ..src.model.issue import Issue

def create_newspapers(agency: Agency):
    paper1 = Newspaper(paper_id=100, name="The New York Times", frequency=7, price=13.14)
    paper2 = Newspaper(paper_id=101, name="Heute", frequency=1, price=1.12)
    paper3 = Newspaper(paper_id=115, name="Wall Street Journal", frequency=1, price=3.00)
    paper4 = Newspaper(paper_id=125, name="National Geographic", frequency=30, price=34.00)
    agency.newspapers.extend([paper1, paper2, paper3, paper4])


def populate(agency: Agency):
    create_newspapers(agency)
    create_editors(agency)
    create_subscribers(agency)
    for newspaer in agency.newspapers:
        create_issues(newspaer)


def create_editors(agency: Agency):
    editor1 = Editor(id=100, name="William Shakespeare")
    editor2 = Editor(id=101, name="Agatha Christie")
    editor3 = Editor(id=102, name="J. K. Rowling")
    editor4 = Editor(id=103, name="Stephen King")
    agency.editors.extend([editor1, editor2, editor3, editor4])


def create_subscribers(agency: Agency):
    subscriber1 = Subscriber(id=100, name = "Sophia Nguyen")
    subscriber2 = Subscriber(id=101, name = "Elijah Patel")
    subscriber3 = Subscriber(id=102, name = "Olivia Mitchell")
    subscriber4 = Subscriber(id=103, name = "Gabriel Taylor")
    agency.subscribers.extend([subscriber1, subscriber2, subscriber3, subscriber4])



def create_issues(newspaper: Newspaper):
    issue1 = Issue(id=100, name="Vol. 1", released=True, releasedate="2022-04-04T00:00:00")
    issue2 = Issue(id=102, name="Vol. 2", released=False, releasedate="2025-05-05T00:00:00")
    newspaper.issues.extend([issue1, issue2])

