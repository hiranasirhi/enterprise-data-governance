from config.database import db
from datetime import datetime

class AuditLog(db.Model):
    __tablename__ = "Audit_Logs"

    log_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("Users.user_id"), nullable=False)
    resource_id = db.Column(db.Integer, db.ForeignKey("Data_Resources.resource_id"), nullable=False)
    action = db.Column(db.String(50), nullable=False)
    risk_score = db.Column(db.Float, default=0.0)
    ip_address = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref="audit_logs")
    resource = db.relationship("DataResource", backref="audit_logs")
