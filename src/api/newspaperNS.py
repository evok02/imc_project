from flask import jsonify, make_response
from flask_restx import Namespace, reqparse, Resource, fields

from ..model.agency import Agency
from ..model.newspaper import Newspaper
from ..model.issue import Issue
from ..model.editor import Editor

from typing import List, Union, Optional

newspaper_ns = Namespace("newspaper", description="Newspaper related operations")


paper_model = newspaper_ns.model('NewspaperModel', {
    'paper_id': fields.Integer(required=False,
            help='The unique identifier of a newspaper'),
    'name': fields.String(required=True,
            help='The name of the newspaper, e.g. The New York Times'),
    'frequency': fields.Integer(required=True,
            help='The publication frequency of the newspaper in days (e.g. 1 for daily papers and 7 for weekly magazines'),
    'price': fields.Float(required=True,
            help='The monthly price of the newspaper (e.g. 12.3)'),
   })

issue_model = newspaper_ns.model("IssueModel", {
    "name": fields.String(required = True,
                          help = "The name of the issue, volume etc."),
    "id": fields.Integer(required = True,
                               help = "The unique identifier of a newspaper"),
    "releasedate": fields.DateTime(required = True, 
                                    help = "The date of the release of this issue"),
    "released": fields.Boolean(required=True)                       
})

editor_model = newspaper_ns.model("EditorModel", {
    "name": fields.String(required = True, 
                          help = "The name of the editor"),
    "id": fields.Integer(required = True,
                         help = "The unique identifier of an editor")
})



@newspaper_ns.route('/')
class NewspaperAPI(Resource):
    _unique_id = 0

    @classmethod
    def _creating_id(cls):
        cls._unique_id += 1
        return cls._unique_id
    
    @newspaper_ns.doc(paper_model, description="Add a new newspaper")
    @newspaper_ns.expect(paper_model, validate=True)
    @newspaper_ns.marshal_with(paper_model, envelope='newspaper')
   

    def post(self):
        # create a new paper object and add it
        new_paper = Newspaper(paper_id=self._creating_id(),
                              name=newspaper_ns.payload['name'],
                              frequency=newspaper_ns.payload['frequency'],
                              price=newspaper_ns.payload['price'])
        Agency.get_instance().add_newspaper(new_paper)

        # return the new paper
        return new_paper

    @newspaper_ns.marshal_list_with(paper_model, envelope='newspapers')
    def get(self):
        return Agency.get_instance().all_newspapers()


@newspaper_ns.route('/<int:paper_id>')
class NewspaperID(Resource):

    @newspaper_ns.doc(description="Get a new newspaper")
    @newspaper_ns.marshal_with(paper_model, envelope='newspaper')
    def get(self, paper_id):
        search_result = Agency.get_instance().get_newspaper(paper_id)
        if not search_result:
            return make_response(f"Newspaper with ID {paper_id} was not found")
        return search_result

    @newspaper_ns.doc(parser=paper_model, description="Update a new newspaper")
    @newspaper_ns.expect(paper_model, validate=True)
    @newspaper_ns.marshal_with(paper_model, envelope='newspaper')
    def post(self, paper_id):
        targeted_paper = Agency.get_instance().get_newspaper(paper_id)
        if not targeted_paper:
            return make_response(f"Newspaper with ID {paper_id} was not found")
        targeted_paper.name = newspaper_ns.payload["name"]
        targeted_paper.frequency = newspaper_ns.payload["frequency"]
        targeted_paper.price = newspaper_ns.payload["price"]
        
        return targeted_paper

    @newspaper_ns.doc(description="Delete a new newspaper")
    def delete(self, paper_id):
        targeted_paper = Agency.get_instance().get_newspaper(paper_id)
        if not targeted_paper:
            return make_response(f"Newspaper with ID {paper_id} was not found")
        Agency.get_instance().remove_newspaper(targeted_paper)
        return jsonify(f"Newspaper with ID {paper_id} was removed")
    

@newspaper_ns.route("/<int:paper_id>/issue")
class NewspaperIssue(Resource):
    @newspaper_ns.doc(description="Get a list of newspaper isssues")
    @newspaper_ns.marshal_with(issue_model, envelope="newspaper")
    def get(self, paper_id):
        targeted_paper = Agency.get_instance().get_newspaper(paper_id)
        if not targeted_paper:
            return make_response(f"Newspaper with ID {paper_id} was not found")
        return targeted_paper.get_issues()
    
        
    @newspaper_ns.doc(parser=issue_model, description="Adding new issue")
    @newspaper_ns.expect(issue_model, validate=True)
    @newspaper_ns.marshal_with(issue_model, envelope='newspaper')
    def post(self, paper_id):
        new_issue = Issue(name = newspaper_ns.payload["name"],
                          id = newspaper_ns.payload["id"],
                          releasedate = newspaper_ns.payload["releasedate"],
                          released = newspaper_ns.payload["released"])
        targeted_paper = Agency.get_instance().get_newspaper(paper_id)
        if not targeted_paper:
            return make_response(f"Newspaper with ID {paper_id} was not found")
        targeted_paper.add_issue(new_issue)
        return new_issue
    
@newspaper_ns.route("/<int:paper_id>/issue/<int:issue_id>")
class IssueID(Resource):
    @newspaper_ns.doc(description = "Get information of a newspaper issue")
    @newspaper_ns.marshal_with(issue_model, envelope = "newspaper")
    def get(self, paper_id, issue_id):
        targeted_paper = Agency.get_instance().get_newspaper(paper_id)
        if not targeted_paper:
            return make_response(f"Newspaper with ID {paper_id} was not found")
        if not targeted_paper.get_issue(issue_id):
            return make_response(f"Newspaper issue with {issue_id} was not found")
        return targeted_paper.get_issue(issue_id)
        
@newspaper_ns.route("/<int:paper_id>/issue/<int:issue_id>/release")
class ReleaseIssue(Resource):
    @newspaper_ns.doc(description = "Release an issue")
    def post(self, paper_id, issue_id):
        targeted_paper = Agency.get_instance().get_newspaper(paper_id)
        if not targeted_paper:
            return make_response(f"Newspaper with ID {paper_id} was not found")
        targeted_issue = targeted_paper.get_issue(issue_id)
        if not targeted_issue:
            return make_response(f"Newspaper issue with {issue_id} was not found")
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
            return make_response(f"Newspaper with ID {paper_id} was not found")
        targeted_issue = targeted_paper.get_issue(issue_id)
        if not targeted_issue:
            return make_response(f"Newspaper issue with {issue_id} was not found")
        targeted_editor = Agency.get_instance().get_editor(editor_id)
        if not targeted_editor: 
            return make_response(f"Issue's editor with ID {editor_id} was not found")
        targeted_issue.set_editor(targeted_editor)
        return jsonify(f"Editor with ID{editor_id} work on {targeted_issue.name}")

@newspaper_ns.route("/<paper_id>/issue/<issue_id>/deliver")
class SendIssue(Resource):
    @newspaper_ns.doc(description = "\"Send\" an issue to a subscriber. This means there should be a record of the subscriber receiving")
    def post(self, paper_id, issue_id, subscriber_id):
        targeted_paper = Agency.get_instance().get_newspaper(paper_id)
        if not targeted_paper:
            return make_response(f"Newspaper with ID {paper_id} was not found")
        targeted_issue = targeted_paper.get_issue(issue_id)
        if not targeted_issue:
            return make_response(f"Newspaper issue with {issue_id} was not found")
        targeted_subscriber = Agency.get_instance().get_subscriebr(subscriber_id)
        if not targeted_subscriber:
            return make_response(f"Newspaper subscriber with {subscriber_id} was not found")
        targeted_issue.send_issue(targeted_subscriber)
        return jsonify(f"Issue was sent to a subscriber with ID {subscriber_id}")
    




        