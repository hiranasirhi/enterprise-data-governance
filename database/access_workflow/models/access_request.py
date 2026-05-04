from config.database import db

class AccessRequest(db.Model):
    __tablename__ = "Access_Requests"

    request_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("Users.user_id"), nullable=False)
    resource_id = db.Column(db.Integer, db.ForeignKey("Data_Resources.resource_id"), nullable=False)
    reason = db.Column(db.Text)
    status = db.Column(db.Enum('Pending', 'Manager Approved', 'Approved', 'Rejected', 'Revoked'), default='Pending')
    requested_at = db.Column(db.DateTime, server_default=db.func.now())

    user = db.relationship("User", backref="access_requests")
    resource = db.relationship("DataResource", backref="access_requests")
