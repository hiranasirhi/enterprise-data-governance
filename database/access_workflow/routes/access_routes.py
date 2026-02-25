from flask import Blueprint
from modules.access_workflow.controllers.access_controller import AccessController

access_bp = Blueprint("access_workflow", __name__)

access_bp.route("/request", methods=["POST"])(AccessController.create_request)
access_bp.route("/manager-approve/<int:request_id>", methods=["PUT"])(AccessController.manager_approve)
access_bp.route("/final-approve/<int:request_id>", methods=["PUT"])(AccessController.final_approve)
access_bp.route("/reject/<int:request_id>", methods=["PUT"])(AccessController.reject)
