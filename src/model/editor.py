from typing import List, Union, Optional
from flask import jsonify, make_response

from .newspaper import Newspaper
from .issue import Issue
from .agency import Agency

class Editor(object):
    def __init__(self, name: str, id: int) -> None:
        self.name = name
        self.id = id
        self.work_on_issues: List[Issue] = []

    
        

    


