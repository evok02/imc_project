from typing import List, Union, Optional
from flask import jsonify, make_response

from .subscriber import Subscriber
class Issue(object):

    def __init__(self, name, id,  releasedate, released: bool = False):
        self.name = name
        self.id = id
        self.releasedate = releasedate
        self.released: bool = released
        self.editor_id = None
        self.send_to: List[Subscriber] = []

    def set_editor(self, editor) -> None:
        self.editor_id = editor.id
        editor.work_on_issues.append(self)

    def send_issue(self, new_subscriber: Subscriber) -> None:
        for subscriber in self.send_to:
            if subscriber.id == new_subscriber.id:
                return make_response(f"Issue was alredy sent to subscriber with ID{subscriber.id}")
        self.send_to.append(new_subscriber)


        
        
        

