from typing import List, Union, Optional
from flask import jsonify, make_response



class Subscriber(object):
    def __init__(self, name, id) -> None:
        self.name = name
        self.id = id
        self.subscribed_newspapers = []
        self.recieved_issued = []