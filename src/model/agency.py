from typing import List, Union, Optional
from flask import jsonify, make_response

from .newspaper import Newspaper
from .editor import Editor
from .subscriber import Subscriber

class Agency(object):
    singleton_instance = None

    def __init__(self):
        self.newspapers: List[Newspaper] = []
        self.editors: List[Editor] = []
        self.subscribers: List[Subscriber] = []
    @staticmethod
    def get_instance():
        if Agency.singleton_instance is None:
            Agency.singleton_instance = Agency()

        return Agency.singleton_instance

    def add_newspaper(self, new_paper: Newspaper):
        #TODO: assert that ID does not exist  yet (or create a new one)
        for newspaper in self.newspapers:
            if newspaper.paper_id == new_paper.paper_id:
                raise ValueError(f'A newspaper with ID {new_paper.paper_id} already exists')
        else:
            self.newspapers.append(new_paper)

    def get_newspaper(self, paper_id: Union[int,str]) -> Optional[Newspaper]:
        for paper in self.newspapers:
            if paper.paper_id == paper_id:
                return paper
        return None

    def all_newspapers(self) -> List[Newspaper]:
        return self.newspapers

    def remove_newspaper(self, paper: Newspaper):
        if paper in self.newspapers:
            self.newspapers.remove(paper)
                

    def get_editors(self):
        return self.editors

    def get_editor(self, editor_id):
        for editor in self.editors:
            if editor.id == editor_id:
                return editor
        return None
    
    def add_editor(self, new_editor: Editor):
        for editor in self.editors:
            if editor.id ==  new_editor.id:
                raise ValueError(f'An editor with ID {new_editor.id} already exists')
        else:
            self.editors.append(new_editor)
    
    def delete_editor(self, editor:Editor) -> None:
        self.editors.remove(editor)

    def get_subscribers(self):
        return self.subscribers
    
    def get_subscriber(self, subscriebr_id):
        for subscruber in self.subscribers:
            if subscruber.id == subscriebr_id:
                return subscruber
        return None
    
    def add_subscriber(self, new_subscriber):
        for subcriber in self.subscribers:
            if subcriber.id ==  new_subscriber.id:
                raise ValueError(f'A subscriber with ID {new_subscriber.id} already exists')
        else:
            self.subscribers.append(new_subscriber)
    def remove_subscriber(self, subscriber):
        if subscriber in self.subscribers:
            self.subscribers.remove(subscriber)

    

    

