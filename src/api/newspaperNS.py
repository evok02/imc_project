from flask import jsonify, make_response
from flask_restx import Namespace, reqparse, Resource, fields

from ..model.agency import Agency
from ..model.newspaper import Newspaper
from ..model.issue import Issue
from ..model.editor import Editor

from typing import List, Union, Optional

import random

newspaper_ns = Namespace("newspaper", description="Newspaper related operations")


paper_post_model = newspaper_ns.model('NewspaperPostModel', {
    'name': fields.String(required=True,
            help='The name of the newspaper, e.g. The New York Times'),
    'frequency': fields.Integer(required=True,
            help='The publication frequency of the newspaper in days (e.g. 1 for daily papers and 7 for weekly magazines'),
    'price': fields.Float(required=True,
            help='The monthly price of the newspaper (e.g. 12.3)')
   })
paper_get_model = newspaper_ns.model('NewspaperGetModel', {
    'paper_id': fields.Integer(required=True,
                         help = 'The unique identifier of the paper'),
    'name': fields.String(required=True,
            help='The name of the newspaper, e.g. The New York Times'),
    'frequency': fields.Integer(required=True,
            help='The publication frequency of the newspaper in days (e.g. 1 for daily papers and 7 for weekly magazines'),
    'price': fields.Float(required=True,
            help='The monthly price of the newspaper (e.g. 12.3)')
   })

issue_post_model = newspaper_ns.model("IssuePostModel", {
    "name": fields.String(required = True,
                          help = "The name of the issue, volume etc."),
    "releasedate": fields.DateTime(required = True, 
                                    help = "The date of the release of this issue"),
    "released": fields.Boolean(required=True)                       
})

issue_get_model = newspaper_ns.model("IssueGetModel", {
    "id": fields.Integer(required = True, 
                         help = "The unique identifier of the editor"),
    "name": fields.String(required = True,
                          help = "The name of the issue, volume etc."),
    "releasedate": fields.DateTime(required = True, 
                                    help = "The date of the release of this issue"),
    "released": fields.Boolean(required=True)  
})

editor_post_model = newspaper_ns.model("EditorPostModel", {
    "name": fields.String(required = True, 
                          help = "The name of the editor")
})
editor_get_model = newspaper_ns.model("EditorGetModel", {
    "id": fields.Integer(readOnly=True, 
                         help="The unique identifier of the editor"),
    "name": fields.String(required = True, 
                          help = "The name of the editor")
})



@newspaper_ns.route('/')
class NewspaperAPI(Resource):
    _paper_unique_ids = set()

    @classmethod
    def _creating_id(cls):
         while True:
            new_id = random.randint(10000000, 99999999)
            if new_id not in cls._paper_unique_ids:
                cls._paper_unique_ids.add(new_id)
                return new_id
    
    @newspaper_ns.doc(paper_post_model, description="Add a new newspaper")
    @newspaper_ns.expect(paper_post_model, validate=True)
    def post(self):
        new_paper_id = self._creating_id()
        # create a new paper object and add it
        new_paper = Newspaper(paper_id=new_paper_id,
                              name=newspaper_ns.payload['name'],
                              frequency=newspaper_ns.payload['frequency'],
                              price=newspaper_ns.payload['price'])
        Agency.get_instance().add_newspaper(new_paper)

        # return the new paper
        return newspaper_ns.marshal(new_paper, paper_get_model)

    @newspaper_ns.marshal_list_with(paper_get_model, envelope='newspapers')
    def get(self):
        return Agency.get_instance().all_newspapers()


@newspaper_ns.route('/<int:paper_id>')
class NewspaperID(Resource):

    @newspaper_ns.doc(description="Get a newspaper")
    def get(self, paper_id):
        search_result = Agency.get_instance().get_newspaper(paper_id)
        if not search_result:
            return jsonify(f"Newspaper with ID {paper_id} was not found")
        return newspaper_ns.marshal(search_result, paper_get_model)

    @newspaper_ns.doc(parser=paper_post_model, description="Update a newspaper")
    @newspaper_ns.expect(paper_post_model, validate=True)
    def post(self, paper_id):
        targeted_paper = Agency.get_instance().get_newspaper(paper_id)
        if not targeted_paper:
            return jsonify(f"Newspaper with ID {paper_id} was not found")
        targeted_paper.name = newspaper_ns.payload["name"]
        targeted_paper.frequency = newspaper_ns.payload["frequency"]
        targeted_paper.price = newspaper_ns.payload["price"]
        
        return newspaper_ns.marshal(targeted_paper, paper_get_model)

    @newspaper_ns.doc(description="Delete a newspaper")
    def delete(self, paper_id):
        targeted_paper = Agency.get_instance().get_newspaper(paper_id)
        if not targeted_paper:
            return jsonify(f"Newspaper with ID {paper_id} was not found")
        Agency.get_instance().remove_newspaper(targeted_paper)
        return jsonify(f"Newspaper with ID {paper_id} was removed")
    

@newspaper_ns.route("/<int:paper_id>/issue")
class NewspaperIssue(Resource):
    _issues_unique_ids = set()
    @classmethod
    def _creating_id(cls):
        while True:
            new_id = random.randint(10000000, 99999999)
            if new_id not in cls._issues_unique_ids:
                cls._issues_unique_ids.add(new_id)
                return new_id
            
    @newspaper_ns.doc(description="Get a list of newspaper isssues")
    
    def get(self, paper_id):
        targeted_paper = Agency.get_instance().get_newspaper(paper_id)
        if not targeted_paper:
            return jsonify(f"Newspaper with ID {paper_id} was not found")
        return newspaper_ns.marshal_list_with(targeted_paper.get_issues(), issue_get_model)
    
        
    @newspaper_ns.doc(parser=issue_post_model, description="Adding new issue")
    @newspaper_ns.expect(issue_post_model, validate=True)
    def post(self, paper_id):
        targeted_paper = Agency.get_instance().get_newspaper(paper_id)
        if not targeted_paper:
            return jsonify(f"Newspaper with ID {paper_id} was not found")
        new_issue = Issue(name = newspaper_ns.payload["name"],
                          id = self._creating_id(),
                          releasedate = newspaper_ns.payload["releasedate"],
                          released = newspaper_ns.payload["released"])
        
        targeted_paper.add_issue(new_issue)
        return newspaper_ns.marshal(new_issue, issue_get_model)
    
@newspaper_ns.route("/<int:paper_id>/issue/<int:issue_id>")
class IssueID(Resource):
    @newspaper_ns.doc(description = "Get information of a newspaper issue")
    @newspaper_ns.marshal_with(issue_get_model, envelope = "newspaper")
    def get(self, paper_id, issue_id):
        targeted_paper = Agency.get_instance().get_newspaper(paper_id)
        if not targeted_paper:
            return jsonify(f"Newspaper with ID {paper_id} was not found")
        if not targeted_paper.get_issue(issue_id):
            return jsonify(f"Newspaper with ID {issue_id} was not found")
        return newspaper_ns.marshal(targeted_paper.get_issue(issue_id), issue_get_model)
        
@newspaper_ns.route("/<int:paper_id>/issue/<int:issue_id>/release")
class ReleaseIssue(Resource):
    @newspaper_ns.doc(description = "Release an issue")
    def post(self, paper_id, issue_id):
        targeted_paper = Agency.get_instance().get_newspaper(paper_id)
        if not targeted_paper:
           return jsonify(f"Newspaper with ID {paper_id} was not found")
        targeted_issue = targeted_paper.get_issue(issue_id)
        if not targeted_issue:
            return jsonify(f"Newspaper with ID {issue_id} was not found")
        targeted_paper.release_issue(issue_id)
        return jsonify(f"Issue was released")


@newspaper_ns.route("/<int:paper_id>/issue/<int:issue_id>/editor")
class SetIssueEditor(Resource):
    @newspaper_ns.doc(description = "Specify an editor for an issue. (Transmit the editor ID as parameter)",
                      params={'editor_id': 'Specify the ID of the editor'})
    def post(self, paper_id, issue_id):
        parser = reqparse.RequestParser()
        parser.add_argument('editor_id', type=int, help='ID of the editor', location='args')
        args = parser.parse_args()
        editor_id = args['editor_id']
        targeted_paper = Agency.get_instance().get_newspaper(paper_id)
        if not targeted_paper:
           return jsonify(f"Newspaper with ID {paper_id} was not found")
        targeted_issue = targeted_paper.get_issue(issue_id)
        if not targeted_issue:
            return jsonify(f"Newspaper with ID {issue_id} was not found")
        targeted_editor = Agency.get_instance().get_editor(editor_id)
        if not targeted_editor: 
            return jsonify(f"Newspaper with ID {editor_id} was not found")
        targeted_issue.set_editor(targeted_editor)
        return jsonify(f"Editor with ID{editor_id} work on {targeted_issue.name}")

@newspaper_ns.route("/<int:paper_id>/issue/<int:issue_id>/deliver")
class SendIssue(Resource):
    @newspaper_ns.doc(description = "\"Send\" an issue to a subscriber. This means there should be a record of the subscriber receiving",
                      params = {"subscriber_id":"Specify the ID of the newspaper"})
    def post(self, paper_id, issue_id):
        parser = reqparse.RequestParser()
        parser.add_argument("subscriber_id",
                            type = int,
                            help = "ID of the newspaper", 
                            location = "args")
        args = parser.parse_args()
        subscriber_id = args["subscriber_id"]
        targeted_paper = Agency.get_instance().get_newspaper(paper_id)
        if not targeted_paper:
           return jsonify(f"Newspaper with ID {paper_id} was not found")
        targeted_issue = targeted_paper.get_issue(issue_id)
        if not targeted_issue:
            return jsonify(f"Newspaper with ID {issue_id} was not found")
        targeted_subscriber = Agency.get_instance().get_subscriebr(subscriber_id)
        if not targeted_subscriber:
            return jsonify(f"Newspaper with ID {subscriber_id} was not found")
        targeted_issue.send_issue(targeted_subscriber)
        return jsonify(f"Issue was sent to a subscriber with ID {subscriber_id}")
    




        