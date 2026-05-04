from config.database import db

class SystemSettings(db.Model):
    __tablename__ = "System_Settings"

    setting_id = db.Column(db.Integer, primary_key=True)
    portal_name = db.Column(db.String(200), default="Enterprise Governance Portal")
    session_timeout = db.Column(db.Integer, default=30)
    risk_score_threshold = db.Column(db.Integer, default=70)
    flag_threshold = db.Column(db.Integer, default=40)
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
