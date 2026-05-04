from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from config.database import db
from database.audit.models.settings_model import SystemSettings
from database.audit.models.admin_model import Admin

settings_bp = Blueprint("settings_bp", __name__)


@settings_bp.route("/", methods=["GET"])
@login_required
def settings():
    system = SystemSettings.query.first()
    return render_template("settings.html", system=system)


@settings_bp.route("/system", methods=["POST"])
@login_required
def update_system():
    system = SystemSettings.query.first()
    system.portal_name = request.form.get("portal_name", "Enterprise Governance Portal")
    system.session_timeout = int(request.form.get("session_timeout", 30))
    db.session.commit()
    flash("System settings updated successfully!", "success")
    return redirect(url_for("settings_bp.settings"))


@settings_bp.route("/notifications", methods=["POST"])
@login_required
def update_notifications():
    system = SystemSettings.query.first()
    system.risk_score_threshold = int(request.form.get("risk_score_threshold", 70))
    system.flag_threshold = int(request.form.get("flag_threshold", 40))
    db.session.commit()
    flash("Notification settings updated successfully!", "success")
    return redirect(url_for("settings_bp.settings"))


@settings_bp.route("/password", methods=["POST"])
@login_required
def change_password():
    current_password = request.form.get("current_password")
    new_password = request.form.get("new_password")
    confirm_password = request.form.get("confirm_password")

    admin = Admin.query.get(current_user.admin_id)

    if not check_password_hash(admin.password_hash, current_password):
        flash("Current password is incorrect!", "error")
        return redirect(url_for("settings_bp.settings"))

    if new_password != confirm_password:
        flash("New passwords do not match!", "error")
        return redirect(url_for("settings_bp.settings"))

    if len(new_password) < 6:
        flash("Password must be at least 6 characters!", "error")
        return redirect(url_for("settings_bp.settings"))

    admin.password_hash = generate_password_hash(new_password)
    db.session.commit()
    flash("Password changed successfully!", "success")
    return redirect(url_for("settings_bp.settings"))
