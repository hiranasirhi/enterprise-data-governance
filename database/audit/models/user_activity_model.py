from config.database import db

class UserActivity(db.Model):
    __tablename__ = "User_Activity"

    activity_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("Users.user_id"), nullable=False)
    resource_id = db.Column(db.Integer, db.ForeignKey("Data_Resources.resource_id"), nullable=False)
    action = db.Column(db.Enum('READ', 'WRITE', 'DELETE', 'UPDATE', 'EXPORT'), nullable=False)
    risk_score = db.Column(db.Float, default=0.0)
    is_flagged = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())

    user = db.relationship("User", backref="activities")
    resource = db.relationship("DataResource", backref="activities")
