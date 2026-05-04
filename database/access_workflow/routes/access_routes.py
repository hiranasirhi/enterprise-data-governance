from flask import Blueprint, render_template, request, redirect, url_for
from database.access_workflow.controllers.access_controller import AccessController
from database.access_workflow.models.access_request import AccessRequest
from flask_login import login_required

access_bp = Blueprint("access_workflow", __name__)

@access_bp.route("/requests", methods=["GET"])
@login_required
def access_requests():
    status_filter = request.args.get("status", "")
    user_filter = request.args.get("user", "")

    query = AccessRequest.query
    if status_filter:
        query = query.filter(AccessRequest.status == status_filter)
    if user_filter:
        query = query.join(AccessRequest.user).filter(
            AccessRequest.user.has(full_name=user_filter)
        )

    all_requests = query.order_by(AccessRequest.requested_at.desc()).all()

    data = [
        {
            "request_id": r.request_id,
            "user": r.user.full_name if r.user else "Unknown",
            "resource": r.resource.resource_name if r.resource else "Unknown",
            "reason": r.reason,
            "status": r.status,
            "requested_at": r.requested_at.strftime("%Y-%m-%d %H:%M") if r.requested_at else ""
        }
        for r in all_requests
    ]

    stats = {
        "total": AccessRequest.query.count(),
        "pending": AccessRequest.query.filter_by(status="Pending").count(),
        "approved": AccessRequest.query.filter_by(status="Approved").count(),
        "rejected": AccessRequest.query.filter_by(status="Rejected").count(),
        "revoked": AccessRequest.query.filter_by(status="Revoked").count(),
    }

    return render_template("access_requests.html", requests=data, stats=stats)


@access_bp.route("/approve/<int:request_id>", methods=["POST"])
@login_required
def approve_request(request_id):
    from config.database import db
    r = AccessRequest.query.get(request_id)
    if r:
        r.status = "Approved"
        db.session.commit()
    return redirect(url_for("access_workflow.access_requests"))


@access_bp.route("/reject/<int:request_id>", methods=["POST"])
@login_required
def reject_request(request_id):
    from config.database import db
    r = AccessRequest.query.get(request_id)
    if r:
        r.status = "Rejected"
        db.session.commit()
    return redirect(url_for("access_workflow.access_requests"))


@access_bp.route("/revoke/<int:request_id>", methods=["POST"])
@login_required
def revoke_request(request_id):
    from config.database import db
    from database.audit.models.audit_model import AuditLog
    r = AccessRequest.query.get(request_id)
    if r:
        r.status = "Revoked"
        audit_entry = AuditLog(
            user_id=r.user_id,
            resource_id=r.resource_id,
            action="ACCESS REVOKED",
            risk_score=95.0,
            ip_address="System"
        )
        db.session.add(audit_entry)
        db.session.commit()
    return redirect(url_for("access_workflow.access_requests"))


access_bp.route("/request", methods=["POST"])(AccessController.create_request)
access_bp.route("/manager-approve/<int:request_id>", methods=["PUT"])(AccessController.manager_approve)
access_bp.route("/final-approve/<int:request_id>", methods=["PUT"])(AccessController.final_approve)
access_bp.route("/reject/<int:request_id>", methods=["PUT"])(AccessController.reject)
