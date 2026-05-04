from database.access_workflow.models.access_request import AccessRequest
from database.access_workflow.models.approval_log import ApprovalLog
from config.database import db
from datetime import datetime, timedelta

class AccessService:

    @staticmethod
    def create_request(user_id, resource_id, manager_id):
        request = AccessRequest(
            user_id=user_id,
            resource_id=resource_id,
            manager_id=manager_id
        )
        db.session.add(request)
        db.session.commit()
        return request

    @staticmethod
    def manager_approve(request_id, manager_id):
        request = AccessRequest.query.get(request_id)

        if request.manager_id != manager_id:
            raise Exception("Unauthorized manager")

        request.status = "MANAGER_APPROVED"

        log = ApprovalLog(
            request_id=request_id,
            approver_id=manager_id,
            action="MANAGER_APPROVED"
        )

        db.session.add(log)
        db.session.commit()
        return request

    @staticmethod
    def final_approve(request_id, approver_id, days_valid=7):
        request = AccessRequest.query.get(request_id)

        request.status = "APPROVED"
        request.final_approver_id = approver_id
        request.approved_at = datetime.utcnow()

        request.access_start = datetime.utcnow()
        request.access_end = datetime.utcnow() + timedelta(days=days_valid)
        request.is_active = True

        log = ApprovalLog(
            request_id=request_id,
            approver_id=approver_id,
            action="FINAL_APPROVED"
        )

        db.session.add(log)
        db.session.commit()
        return request

    @staticmethod
    def reject(request_id, approver_id):
        request = AccessRequest.query.get(request_id)

        request.status = "REJECTED"

        log = ApprovalLog(
            request_id=request_id,
            approver_id=approver_id,
            action="REJECTED"
        )

        db.session.add(log)
        db.session.commit()
        return request

    @staticmethod
    def check_expired_access():
        now = datetime.utcnow()
        expired = AccessRequest.query.filter(
            AccessRequest.access_end < now,
            AccessRequest.is_active == True
        ).all()

        for req in expired:
            req.status = "EXPIRED"
            req.is_active = False

        db.session.commit()
