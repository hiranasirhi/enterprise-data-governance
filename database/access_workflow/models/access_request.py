from config.database import db
from datetime import datetime

class AccessRequest(db.Model):
    __tablename__ = "Access_Requests"

    request_id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("Users.user_id"), nullable=False)
    resource_id = db.Column(db.Integer, db.ForeignKey("Data_Resources.resource_id"), nullable=False)

    status = db.Column(db.String(30), default="PENDING")

    manager_id = db.Column(db.Integer, db.ForeignKey("Users.user_id"))
    final_approver_id = db.Column(db.Integer, db.ForeignKey("Users.user_id"))

    requested_at = db.Column(db.DateTime, default=datetime.utcnow)
    approved_at = db.Column(db.DateTime)

    access_start = db.Column(db.DateTime)
    access_end = db.Column(db.DateTime)

    is_active = db.Column(db.Boolean, default=False)
