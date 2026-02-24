from config.database import db
from datetime import datetime

class AccessRequest(db.Model):
    __tablename__ = "access_requests"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    resource_id = db.Column(db.Integer, nullable=False)

    status = db.Column(db.String(20), default="PENDING")
    requested_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviewed_at = db.Column(db.DateTime)
    reviewed_by = db.Column(db.Integer)
