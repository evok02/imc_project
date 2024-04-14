from typing import List

from flask_restx import Model

from .issue import Issue

from flask import jsonify

from typing import List, Union, Optional

from .subscriber import Subscriber

import datetime


class Newspaper(object):

    def __init__(self, paper_id: int, name: str, frequency: int, price: float):
        self.paper_id: int = paper_id
        self.name: str = name
        self.frequency: int = frequency  # the issue frequency (in days)
        self.price: float = price  # the monthly price
        self.issues: List[Issue] = []


    def get_issues(self) -> List[Issue]:
        return self.issues


    def add_issue(self, new_issue: Issue) -> None:
        for issue in self.issues:
            if issue.id == new_issue.id:
                raise ValueError(f"Newspaper with ID {new_issue.id} already exists")
        else: 
            self.issues.append(new_issue)
            new_issue.newspaper = self

    def get_issue(self, issue_id:int) -> Optional[Issue]:
        for issue in self.issues:
            if issue.id == issue_id:
                return issue
        return None
    
    def release_issue(self, issue_id: int) -> None:
        for issue in self.issues:
            if issue.id == issue_id:
                if issue.released == False:
                    issue.released = True
                    issue.releasedate = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
                else: 
                    return jsonify(f"Issue was released {issue.releasedate}")
                
    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return self.name
                

            


