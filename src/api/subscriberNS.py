from flask import jsonify, make_response
from flask_restx import Namespace, reqparse, Resource, fields

from ..model.agency import Agency
from ..model.newspaper import Newspaper
from ..model.issue import Issue
from ..model.editor import Editor
from ..model.subscriber import Subscriber

from typing import List, Union, Optional

import random


subscriber_ns = Namespace("subscriber", description="Subscriber related operations")

editor_post_model = subscriber_ns.model("EditorPostodel", {
    "name": fields.String(required = True, 
                          help = "The name of the editor")
})
editor_get_model = subscriber_ns.model("EditorGetModel", {
    "id": fields.Integer(readOnly=True, 
                         help="The unique identifier of the editor"),
    "name": fields.String(required = True, 
                          help = "The name of the editor")
})
subscriber_post_model = subscriber_ns.model("SubscriberPostModel", {
    "name": fields.String(required = True, 
                          help = "The name of the editor")
})
subscriber_get_model = subscriber_ns.model("SubscriberGetModel", {
    "name": fields.String(required = True, 
                          help = "The name of the editor"),
    "id": fields.Integer(required = True,
                         help = "The unique identifier of an editor")
})


@subscriber_ns.route("/")
class SubscriberAPI(Resource):
    _subscribers_unique_ids = set()

    @classmethod
    def _creating_id(cls):
        while True:
            new_id = random.randint(10000000, 99999999)
            if new_id not in cls._subscribers_unique_ids:
                cls._subscribers_unique_ids.add(new_id)
                return new_id
    
    @subscriber_ns.marshal_list_with(subscriber_get_model, envelope = "subscribers")
    def get(self):
        return Agency.get_instance().get_subscribers()
    @subscriber_ns.doc(subscriber_get_model, description = "Add a new subscriber")
    @subscriber_ns.expect(subscriber_post_model, validate = True)
    @subscriber_ns.marshal_with(subscriber_get_model, envelope = "subscriber")
    def post(self):
        new_subscriber = Subscriber(id=self._creating_id(),
                              name=subscriber_ns.payload['name'])
        Agency.get_instance().add_subscriber(new_subscriber)

        # return the new paper
        return new_subscriber
    
@subscriber_ns.route("/<int:subscriber_id>")
class SubscriberID(Resource):
    def get(self, subscriber_id):
        targeted_subscriber = Agency.get_instance().get_subscriber(subscriber_id)
        if not targeted_subscriber:
            return jsonify(f"Subscriber with ID {subscriber_id} was not found")
        return subscriber_ns.marshal(targeted_subscriber, subscriber_get_model)
    
    @subscriber_ns.doc(parser = subscriber_post_model, description = "Update a subscriber information")
    @subscriber_ns.expect(subscriber_post_model, validate = True)
    def post(self, subscriber_id):
        targeted_subscriber = Agency.get_instance().get_subscriber(subscriber_id)
        if not targeted_subscriber:
            return jsonify(f"Subscriber with ID {subscriber_id} was not found")
        targeted_subscriber.name = subscriber_ns.payload["name"]
        return subscriber_ns.marshal(targeted_subscriber, subscriber_get_model)
    @subscriber_ns.doc(description = "Delete a subscriber")
    def delete(self, subscriber_id):
        targeted_subscriber = Agency.get_instance().get_subscriber(subscriber_id)
        if not targeted_subscriber:
            return jsonify(f"Subscriber with ID {subscriber_id} was not found")
        Agency.get_instance().remove_subscriber(targeted_subscriber)
        return jsonify(f"Subscriber with ID {subscriber_id} was removed")
    
@subscriber_ns.route("/<int:subscriber_id>/subscribe")
class SubscriberSubscribe(Resource):
    @subscriber_ns.doc(description = "Subscribe a subscriber to a newspaper. (Transmit the newspaper ID as parameter.)",
                       params = {"paper_id":"Specify the ID of the newspaper"})
    def post(self, subscriber_id):
        parser = reqparse.RequestParser()
        parser.add_argument("paper_id",
                            type = int,
                            help = "ID of the newspaper", 
                            location = "args")
        args = parser.parse_args()
        paper_id = args["paper_id"]
        targeted_subscriber = Agency.get_instance().get_subscriber(subscriber_id)
        if not targeted_subscriber:
            return jsonify(f"Subscriber with ID {subscriber_id} was not found")
        targeted_paper = Agency.get_instance().get_newspaper(paper_id)
        if not targeted_paper:
            return jsonify(f"Newspaper with ID {paper_id} was not found")
        targeted_subscriber.subscribe(targeted_paper)
        return jsonify(f"Subscriber was subscribed to a newspaper")

@subscriber_ns.route("/<int:subscriber_id>/stats")
class SubscriberStats(Resource):
    @subscriber_ns.doc(description = "Get the number of newspaper subscriptions and the monthly and annual cost, as well as the number of issues that the subscriber received for each paper.")
    def get(self, subscriber_id):
        targeted_subscriber = Agency.get_instance().get_subscriber(subscriber_id)
        if not targeted_subscriber:
            return jsonify(f"Subscriber with ID {subscriber_id} was not found")
        return targeted_subscriber.create_stats()
    
@subscriber_ns.route("/subscriber/<int:subscriber_id>/missingissues")
class SubscriberMissingIssues(Resource):
    @subscriber_ns.doc(description = "Check if there are any undelivered issues of the subscribed newspapers")
    def get(self, subscriber_id):
        targeted_subscriber = Agency.get_instance().get_subscriber(subscriber_id)
        if not targeted_subscriber:
            return jsonify(f"Subscriber with ID {subscriber_id} was not found")
        return targeted_subscriber.check_missing_issues()




