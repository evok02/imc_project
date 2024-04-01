from typing import List

from flask_restx import Model

from .issue import Issue

from flask import jsonify


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
                return jsonify(f"Issue of this newspaper with ID {new_issue.id} already exist. Try another one")
        else: 
            self.issues.append(new_issue)
