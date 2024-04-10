from typing import List, Union, Optional
from flask import jsonify, make_response



class Subscriber(object):
    def __init__(self, name, id) -> None:
        self.name = name
        self.id = id
        self.subscribed_newspapers = []
        self.recieved_issues = []

    def subscribe(self, newspaper):
        self.subscribed_newspapers.append(newspaper)

    def create_stats(self):
        newspapers = len(self.subscribed_newspapers)
        monthly_cost = 0
        for paper in self.subscribed_newspapers:
            monthly_cost += paper.price
        annual_cost = 12 * monthly_cost
        num_of_issues = {}
        for issue in  self.recieved_issues:
            if issue.newspaper not in num_of_issues.keys():
                num_of_issues[issue.newspaper] = 1
            else:
                num_of_issues[issue.newspaper] += 1
        return {
            "Number of subscribed newspapers": newspapers,
            "Monthly cost": monthly_cost,
            "Annual cost": annual_cost, 
            "Number of issues that the subscriber received for each paper":num_of_issues
        }
    
    def check_missing_issues(self):
        missing_issues = []
        for newspaper in self.subscribed_newspapers:
            for issue in newspaper.issues:
                if issue not in self.recieved_issues:
                    missing_issues.append(issue.name)
                    issue.send_issue(self)
        if len(missing_issues) != 0:
            return f"Issues {missing_issues} were sent to a subscriber"
        else:
            return f"There are no missing issues"
        


    