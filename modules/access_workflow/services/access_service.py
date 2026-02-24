from modules.access_workflow.models.access_request import AccessRequest
from config.database import db
from datetime import datetime

class AccessService:

    @staticmethod
    def create_request(user_id, resource_id):
        request = AccessRequest(
            user_id=user_id,
            resource_id=resource_id
        )
        db.session.add(request)
        db.session.commit()
        return request

    @staticmethod
    def approve_request(request_id, admin_id):
        request = AccessRequest.query.get(request_id)
        request.status = "APPROVED"
        request.reviewed_by = admin_id
        request.reviewed_at = datetime.utcnow()
        db.session.commit()
        return request

    @staticmethod
    def reject_request(request_id, admin_id):
        request = AccessRequest.query.get(request_id)
        request.status = "REJECTED"
        request.reviewed_by = admin_id
        request.reviewed_at = datetime.utcnow()
        db.session.commit()
        return request
