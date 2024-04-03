from typing import List, Union, Optional
from flask import jsonify, make_response

from .issue import Issue

class Editor(object):
    def __init__(self, name: str, id: int) -> None:
        self.name = name
        self.id = id
        self.work_on_issues: List[Issue] = []

    def get_issues(self):
        return self.work_on_issues

    
        

    


