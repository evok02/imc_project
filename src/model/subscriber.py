from typing import List, Union, Optional
from flask import jsonify, make_response

from .newspaper import Newspaper
from .issue import Issue
from .agency import Agency

class Subscriber(object):
    def __init__(self, name, id) -> None:
        self.name = name
        self.id = id
        self.subscribed_newspapers: List[Newspaper] = []
        self.recieved_issued: List[Issue] = []