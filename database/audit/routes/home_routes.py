from flask import Blueprint, render_template
from database.audit.models.audit_model import AuditLog
from database.audit.models.user_model import User
from database.audit.models.user_activity_model import UserActivity
from database.access_workflow.models.access_request import AccessRequest
from config.database import db
from flask_login import login_required

home_bp = Blueprint("home_bp", __name__)

@home_bp.route("/")
@login_required
def home():
    # Stats
    stats = {
        "total_users": User.query.count(),
        "total_logs": AuditLog.query.count(),
        "flagged": UserActivity.query.filter_by(is_flagged=True).count(),
        "blocked_users": User.query.filter_by(is_blocked=True).count(),
        "pending_requests": AccessRequest.query.filter_by(status="Pending").count(),
        "high_risk": UserActivity.query.filter(UserActivity.risk_score >= 70).count(),
    }

    # Pie chart — action breakdown
    actions = ["READ", "WRITE", "DELETE", "UPDATE", "EXPORT"]
    action_counts = [
        UserActivity.query.filter_by(action=a).count() for a in actions
    ]

    # Bar chart — risk scores of recent activities
    recent_activities = UserActivity.query.order_by(
        UserActivity.timestamp.desc()
    ).limit(7).all()

    bar_labels = [
        f"{a.user.full_name} - {a.action}" if a.user else a.action
        for a in recent_activities
    ]
    bar_scores = [a.risk_score for a in recent_activities]

    # Recent activity table
    recent = [
        {
            "user": a.user.full_name if a.user else "Unknown",
            "resource": a.resource.resource_name if a.resource else "Unknown",
            "action": a.action,
            "risk_score": a.risk_score,
            "is_flagged": a.is_flagged,
            "timestamp": a.timestamp.strftime("%Y-%m-%d %H:%M") if a.timestamp else ""
        }
        for a in recent_activities
    ]

    # Users with their roles
    user_roles_query = db.session.execute(db.text("""
        SELECT u.full_name, u.email, r.role_name, d.dept_name,
               CASE WHEN u.is_blocked THEN 'Blocked' ELSE 'Active' END as status
        FROM Users u
        LEFT JOIN User_Roles ur ON u.user_id = ur.user_id
        LEFT JOIN Roles r ON ur.role_id = r.role_id
        LEFT JOIN Departments d ON u.dept_id = d.dept_id
    """)).fetchall()

    user_roles = [
        {
            "full_name": row[0],
            "email": row[1],
            "role_name": row[2] or "No Role",
            "dept_name": row[3] or "No Department",
            "status": row[4]
        }
        for row in user_roles_query
    ]

    # Role permissions
    role_perms_query = db.session.execute(db.text("""
        SELECT r.role_name, p.action, dr.resource_name, dr.sensitivity_level
        FROM Roles r
        JOIN Role_Permissions rp ON r.role_id = rp.role_id
        JOIN Permissions p ON rp.permission_id = p.permission_id
        JOIN Data_Resources dr ON p.resource_id = dr.resource_id
        ORDER BY r.role_name
    """)).fetchall()

    role_permissions = [
        {
            "role_name": row[0],
            "action": row[1],
            "resource_name": row[2],
            "sensitivity_level": row[3]
        }
        for row in role_perms_query
    ]

    # Extra stats
    role_stats = {
        "total_roles": db.session.execute(db.text("SELECT COUNT(*) FROM Roles")).scalar(),
        "total_permissions": db.session.execute(db.text("SELECT COUNT(*) FROM Permissions")).scalar(),
        "total_resources": db.session.execute(db.text("SELECT COUNT(*) FROM Data_Resources")).scalar(),
    }

    return render_template(
        "home.html",
        stats=stats,
        action_labels=actions,
        action_counts=action_counts,
        bar_labels=bar_labels,
        bar_scores=bar_scores,
        recent=recent,
        user_roles=user_roles,
        role_permissions=role_permissions,
        role_stats=role_stats
    )
