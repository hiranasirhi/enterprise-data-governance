from flask import request, jsonify
from database.access_workflow.services.access_service import AccessService
from database.access_workflow.validators.access_validator import validate_request

class AccessController:

    @staticmethod
    def create_request():
        data = request.get_json()

        if not validate_request(data):
            return jsonify({"error": "Invalid data"}), 400

        request_obj = AccessService.create_request(
            data["user_id"],
            data["resource_id"],
            data["manager_id"]
        )

        return jsonify({
            "message": "Request submitted",
            "request_id": request_obj.request_id
        }), 201

    @staticmethod
    def manager_approve(request_id):
        manager_id = request.get_json()["manager_id"]
        AccessService.manager_approve(request_id, manager_id)
        return jsonify({"message": "Manager approved"})

    @staticmethod
    def final_approve(request_id):
        data = request.get_json()
        AccessService.final_approve(request_id, data["approver_id"], data.get("days_valid", 7))
        return jsonify({"message": "Access granted"})

    @staticmethod
    def reject(request_id):
        approver_id = request.get_json()["approver_id"]
        AccessService.reject(request_id, approver_id)
        return jsonify({"message": "Request rejected"})
