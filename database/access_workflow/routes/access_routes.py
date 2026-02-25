from flask import Blueprint
from modules.access_workflow.controllers.access_controller import AccessController

access_bp = Blueprint("access_workflow", __name__)

access_bp.route("/request", methods=["POST"])(AccessController.create)
access_bp.route("/approve/<int:request_id>", methods=["PUT"])(AccessController.approve)
access_bp.route("/reject/<int:request_id>", methods=["PUT"])(AccessController.reject)
