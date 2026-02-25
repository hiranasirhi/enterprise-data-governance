class ApprovalLog(db.Model):
    __tablename__ = "approval_logs"

    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, nullable=False)
    approver_id = db.Column(db.Integer, nullable=False)
    action = db.Column(db.String(20))  # APPROVED / REJECTED
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
