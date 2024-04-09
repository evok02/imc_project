from flask import jsonify, make_response
from flask_restx import Namespace, reqparse, Resource, fields

from ..model.agency import Agency
from ..model.newspaper import Newspaper
from ..model.issue import Issue
from ..model.editor import Editor

from typing import List, Union, Optional

editor_ns = Namespace("editor", description = "Editor related operations")

issue_model = editor_ns.model("IssueModel", {
    "name": fields.String(required = True,
                          help = "The name of the issue, volume etc."),
    "id": fields.Integer(required = True,
                               help = "The unique identifier of a newspaper"),
    "releasedate": fields.DateTime(required = True, 
                                    help = "The date of the release of this issue"),
    "released": fields.Boolean(required=True)                       
})

editor_model = editor_ns.model("EditorModel", {
    "name": fields.String(required = True, 
                          help = "The name of the editor"),
    "id": fields.Integer(required = True,
                         help = "The unique identifier of an editor")
})


@editor_ns.route("/")
class EditorAPI(Resource):
    @editor_ns.doc(description = "Get a list of all editors")
    @editor_ns.marshal_list_with(editor_model, envelope='editor')
    def get(self):
        return Agency.get_instance().get_editors()
    

    @editor_ns.doc(editor_model, description="Add a new editor")
    @editor_ns.expect(editor_model, validate=True)
    @editor_ns.marshal_with(editor_model, envelope='newspaper')
    def post(self):
        new_editor = Editor(id=editor_ns.payload["id"],
                              name=editor_ns.payload["name"])   
        Agency.get_instance().add_editor(new_editor)

        return new_editor
    
@editor_ns.route("/<int:editor_id>")
class EditorID(Resource):
    @editor_ns.doc(description = "Get an editor's information")
    @editor_ns.marshal_with(editor_model, envelope = "editor")
    def get(self, editor_id):
        targeted_editor = Agency.get_instance().get_editor(editor_id)
        if not targeted_editor:
            return make_response(f"Editor with ID {editor_id} was not found")
        return targeted_editor
    @editor_ns.doc(description = "Update an editor's information")
    @editor_ns.expect(editor_model, validate = True)
    @editor_ns.marshal_with(editor_model, envelope = "editor")
    def post(self, editor_id):
        targeted_editor = Agency.get_instance().get_editor(editor_id)
        if not targeted_editor:
            return make_response(f"Editor with ID {editor_id} was not found")
        targeted_editor.name = editor_ns.payload["name"]
        targeted_editor.id = editor_ns.payload["id"]
        return targeted_editor
    @editor_ns.doc(description = "Delete an editor")
    def delete(self, editor_id):
        targeted_editor = Agency.get_instance().get_editor(editor_id)
        if not targeted_editor:
            return make_response(f"Editor with ID {editor_id} was not found")
        Agency.get_instance().delete_editor(targeted_editor)
        return make_response(f"Ediot with ID {editor_id} was deleted")
    
@editor_ns.route("/<int:editor_id>/issues")
class EditorIssues(Resource):
    @editor_ns.doc(description = "Return a list of newapaper issues that the editor was responsible for")
    @editor_ns.marshal_list_with(issue_model, envelope = "editor")
    def get(self, editor_id) -> List[Issue]:
        targeted_editor = Agency.get_instance().get_editor(editor_id)
        if not targeted_editor:
            return make_response(f"Editor with ID {editor_id} was not found")
        return targeted_editor.get_issues()