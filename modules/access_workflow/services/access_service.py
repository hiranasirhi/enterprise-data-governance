from modules.access_workflow.models.access_request import AccessRequest
from config.database import db
from datetime import datetime, timedelta

class AccessService:

    @staticmethod
    def create_request(employee_id, resource_id, manager_id, reason):
        request = AccessRequest(
            employee_id=employee_id,
            resource_id=resource_id,
            manager_id=manager_id,
            reason=reason
        )
        db.session.add(request)
        db.session.commit()
        return request

    @staticmethod
    def manager_approve(request_id, manager_id):
        request = AccessRequest.query.get(request_id)

        if request.manager_id != manager_id:
            raise Exception("Unauthorized approval")

        request.status = "MANAGER_APPROVED"
        db.session.commit()
        return request

    @staticmethod
    def final_approve(request_id, admin_id, days_valid=7):
        request = AccessRequest.query.get(request_id)

        request.status = "APPROVED"
        request.approved_by = admin_id
        request.approved_at = datetime.utcnow()

        request.access_start = datetime.utcnow()
        request.access_end = datetime.utcnow() + timedelta(days=days_valid)

        request.is_active = True

        db.session.commit()
        return request

    @staticmethod
    def reject(request_id, reviewer_id):
        request = AccessRequest.query.get(request_id)

        request.status = "REJECTED"
        request.approved_by = reviewer_id
        request.approved_at = datetime.utcnow()

        db.session.commit()
        return request

    @staticmethod
    def check_expired_access():
        now = datetime.utcnow()
        expired_requests = AccessRequest.query.filter(
            AccessRequest.access_end < now,
            AccessRequest.is_active == True
        ).all()

        for req in expired_requests:
            req.status = "EXPIRED"
            req.is_active = False

        db.session.commit()
