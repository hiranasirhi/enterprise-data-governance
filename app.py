import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from flask import Flask, render_template, redirect
from flask_login import LoginManager
from config.database import db
from config.config import Config

# Import blueprints
from database.access_workflow.routes.access_routes import access_bp
from database.audit.routes.audit_routes import audit_bp
from database.audit.routes.activity_routes import activity_bp
from database.audit.routes.home_routes import home_bp
from database.audit.routes.auth_routes import auth_bp
from database.audit.routes.settings_routes import settings_bp
from database.audit.routes.ai_reports_routes import ai_reports_bp


# Import all models so SQLAlchemy knows about them
from database.audit.models.audit_model import AuditLog
from database.audit.models.user_model import User
from database.audit.models.resource_model import DataResource
from database.audit.models.user_activity_model import UserActivity
from database.audit.models.department_model import Department
from database.audit.models.admin_model import Admin
from database.access_workflow.models.access_request import AccessRequest
from database.audit.models.settings_model import SystemSettings

# Create Flask app
app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "shared", "templates"),
    static_folder=os.path.join(BASE_DIR, "shared", "static"),
    static_url_path="/static"
)

app.config.from_object(Config)
app.config["SECRET_KEY"] = "govportal-secret-2026"
db.init_app(app)

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth_bp.login"
login_manager.login_message = "Please login to access the portal."
login_manager.login_message_category = "error"

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

# Register blueprints
app.register_blueprint(auth_bp,     url_prefix="/auth")
app.register_blueprint(access_bp,   url_prefix="/access")
app.register_blueprint(audit_bp,    url_prefix="/audit")
app.register_blueprint(activity_bp, url_prefix="/activity")
app.register_blueprint(home_bp,     url_prefix="/home")
app.register_blueprint(settings_bp, url_prefix="/settings")
app.register_blueprint(ai_reports_bp, url_prefix="/ai-reports")

# Root route
@app.route("/")
def dashboard():
    return redirect("/home/")

# Test route
@app.route("/test-static")
def test_static():
    return """
    <link rel="stylesheet" href="/static/AdminLTE/dist/css/adminlte.min.css">
    <h1 style="color:green;">AdminLTE Static Working</h1>
    """

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
