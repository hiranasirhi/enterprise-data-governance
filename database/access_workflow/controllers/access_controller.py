from flask import request, jsonify
from modules.access_workflow.services.access_service import AccessService

class AccessController:

    @staticmethod
    def create():
        data = request.get_json()
        user_id = data["user_id"]
        resource_id = data["resource_id"]

        request_obj = AccessService.create_request(user_id, resource_id)

        return jsonify({
            "message": "Access request created",
            "id": request_obj.id
        }), 201

    @staticmethod
    def approve(request_id):
        admin_id = request.get_json()["admin_id"]
        request_obj = AccessService.approve_request(request_id, admin_id)

        return jsonify({"message": "Access approved"})

    @staticmethod
    def reject(request_id):
        admin_id = request.get_json()["admin_id"]
        request_obj = AccessService.reject_request(request_id, admin_id)

        return jsonify({"message": "Access rejected"})
