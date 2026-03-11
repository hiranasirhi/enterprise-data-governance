from config.database import db
from datetime import datetime

class ApprovalLog(db.Model):
    __tablename__ = "Approval_Logs"

    log_id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey("Access_Requests.request_id"))
    approver_id = db.Column(db.Integer, db.ForeignKey("Users.user_id"))
    action = db.Column(db.String(20))  # APPROVED / REJECTED
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
