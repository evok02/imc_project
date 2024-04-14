from flask import jsonify, make_response
from flask_restx import Namespace, reqparse, Resource, fields

from ..model.agency import Agency
from ..model.newspaper import Newspaper
from ..model.issue import Issue
from ..model.editor import Editor

from typing import List, Union, Optional

import random

editor_ns = Namespace("editor", description = "Editor related operations")

issue_post_model = editor_ns.model("IssuePostModel", {
    "name": fields.String(required = True,
                          help = "The name of the issue, volume etc."),
    "releasedate": fields.DateTime(required = True, 
                                    help = "The date of the release of this issue"),
    "released": fields.Boolean(required=True)                       
})

issue_get_model = editor_ns.model("IssueGetModel", {
    "id": fields.Integer(required = True, 
                         help = "The unique identifier of the editor"),
    "name": fields.String(required = True,
                          help = "The name of the issue, volume etc."),
    "releasedate": fields.DateTime(required = True, 
                                    help = "The date of the release of this issue"),
    "released": fields.Boolean(required=True)  
})

editor_post_model = editor_ns.model("EditorPostModel", {
    "name": fields.String(required = True, 
                          help = "The name of the editor")
})
editor_get_model = editor_ns.model("EditorGetModel", {
    "id": fields.Integer(readOnly=True, 
                         help="The unique identifier of the editor"),
    "name": fields.String(required = True, 
                          help = "The name of the editor")
})


@editor_ns.route("/")
class EditorAPI(Resource):
    _editors_unique_ids = set()

    @classmethod
    def _creating_id(cls):
        while True:
            new_id = random.randint(10000000, 99999999)
            if new_id not in cls._editors_unique_ids:
                cls._editors_unique_ids.add(new_id)
                return new_id
    
    @editor_ns.doc(description = "Get a list of all editors")
    @editor_ns.marshal_list_with(editor_get_model, envelope = "editor")
    def get(self):
        return Agency.get_instance().get_editors()
    

    @editor_ns.doc(editor_post_model, description="Add a new editor")
    @editor_ns.expect(editor_post_model, validate=True)
    def post(self):
        new_editor = Editor(id=self._creating_id(),
                              name=editor_ns.payload["name"])   
        Agency.get_instance().add_editor(new_editor)

        return editor_ns.marshal(new_editor, editor_get_model)
    
@editor_ns.route("/<int:editor_id>")
class EditorID(Resource):
    @editor_ns.doc(description = "Get an editor's information")
    def get(self, editor_id):
        targeted_editor = Agency.get_instance().get_editor(editor_id)
        if not targeted_editor:
            return jsonify(f"Editor with ID {editor_id} was not found")
        return editor_ns.marshal(targeted_editor, editor_get_model)
    @editor_ns.doc(description = "Update an editor's information")
    @editor_ns.expect(editor_post_model, validate = True)
    def post(self, editor_id):
        targeted_editor = Agency.get_instance().get_editor(editor_id)
        if not targeted_editor:
            return jsonify(f"Editor with ID {editor_id} was not found")
        targeted_editor.name = editor_ns.payload["name"]
        return editor_ns.marshal(targeted_editor, editor_get_model)
    @editor_ns.doc(description = "Delete an editor")
    def delete(self, editor_id):
        targeted_editor = Agency.get_instance().get_editor(editor_id)
        if not targeted_editor:
            return jsonify(f"Editor with ID {editor_id} was not found")
        Agency.get_instance().delete_editor(targeted_editor)
        return jsonify(f"Editor with ID {editor_id} was deleted")
    
@editor_ns.route("/<int:editor_id>/issues")
class EditorIssues(Resource):
    @editor_ns.doc(description = "Return a list of newapaper issues that the editor was responsible for")
    
    def get(self, editor_id) -> List[Issue]:
        targeted_editor = Agency.get_instance().get_editor(editor_id)
        if not targeted_editor:
            return jsonify(f"Editor with ID {editor_id} was not found")
        return editor_ns.marshal(targeted_editor.get_issues(), issue_get_model)