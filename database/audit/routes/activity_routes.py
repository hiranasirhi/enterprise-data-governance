from flask import Blueprint, render_template, request, redirect, url_for
from config.database import db
from database.audit.models.user_activity_model import UserActivity
from database.audit.models.user_model import User
from database.audit.models.audit_model import AuditLog
from datetime import datetime
from flask_login import login_required

activity_bp = Blueprint("activity_bp", __name__)

@activity_bp.route("/", methods=["GET"])
@login_required
def user_activity():
    status_filter = request.args.get("status", "")
    action_filter = request.args.get("action", "")

    query = UserActivity.query
    if status_filter == "flagged":
        query = query.filter(UserActivity.is_flagged == True)
    if action_filter:
        query = query.filter(UserActivity.action == action_filter)

    activities = query.order_by(UserActivity.timestamp.desc()).all()

    data = [
        {
            "activity_id": a.activity_id,
            "user_id": a.user_id,
            "user": a.user.full_name if a.user else "Unknown",
            "is_blocked": a.user.is_blocked if a.user else False,
            "resource": a.resource.resource_name if a.resource else "Unknown",
            "action": a.action,
            "risk_score": a.risk_score,
            "is_flagged": a.is_flagged,
            "timestamp": a.timestamp.strftime("%Y-%m-%d %H:%M") if a.timestamp else ""
        }
        for a in activities
    ]

    stats = {
        "total": UserActivity.query.count(),
        "flagged": UserActivity.query.filter_by(is_flagged=True).count(),
        "high_risk": UserActivity.query.filter(UserActivity.risk_score >= 70).count(),
        "blocked_users": User.query.filter_by(is_blocked=True).count(),
    }

    return render_template("user_activity.html", activities=data, stats=stats)


@activity_bp.route("/block/<int:user_id>", methods=["POST"])
@login_required
def block_user(user_id):
    reason = request.form.get("reason", "Suspicious activity detected")
    user = User.query.get(user_id)
    if user:
        user.is_blocked = True
        user.blocked_reason = reason
        user.blocked_at = datetime.utcnow()
        activities = UserActivity.query.filter_by(user_id=user_id).first()
        if activities:
            audit_entry = AuditLog(
                user_id=user_id,
                resource_id=activities.resource_id,
                action="USER BLOCKED",
                risk_score=100.0,
                ip_address="System"
            )
            db.session.add(audit_entry)
        db.session.commit()
    return redirect(url_for("activity_bp.user_activity"))


@activity_bp.route("/unblock/<int:user_id>", methods=["POST"])
@login_required
def unblock_user(user_id):
    user = User.query.get(user_id)
    if user:
        user.is_blocked = False
        user.blocked_reason = None
        user.blocked_at = None
        activities = UserActivity.query.filter_by(user_id=user_id).first()
        if activities:
            audit_entry = AuditLog(
                user_id=user_id,
                resource_id=activities.resource_id,
                action="USER UNBLOCKED",
                risk_score=20.0,
                ip_address="System"
            )
            db.session.add(audit_entry)
        db.session.commit()
    return redirect(url_for("activity_bp.user_activity"))
