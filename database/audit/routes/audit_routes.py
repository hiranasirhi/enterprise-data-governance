from flask import Blueprint, render_template
from database.audit.controller.audit_controller import get_audit_dashboard_data
from flask_login import login_required

audit_bp = Blueprint(
    "audit_bp",
    __name__,
    template_folder="../../../shared/templates"
)

@audit_bp.route("/")
@login_required
def audit_dashboard():
    data = get_audit_dashboard_data()
    return render_template("audit_dashboard.html", logs=data["logs"], stats=data["stats"])
