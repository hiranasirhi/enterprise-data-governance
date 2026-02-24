from config.database import db
from datetime import datetime

class AccessRequest(db.Model):
    __tablename__ = "access_requests"

    id = db.Column(db.Integer, primary_key=True)

    employee_id = db.Column(db.Integer, nullable=False)
    resource_id = db.Column(db.Integer, nullable=False)

    status = db.Column(db.String(30), default="PENDING")

    manager_id = db.Column(db.Integer, nullable=False)
    approved_by = db.Column(db.Integer)

    requested_at = db.Column(db.DateTime, default=datetime.utcnow)
    approved_at = db.Column(db.DateTime)

    access_start = db.Column(db.DateTime)
    access_end = db.Column(db.DateTime)

    reason = db.Column(db.Text)

    is_active = db.Column(db.Boolean, default=False)
