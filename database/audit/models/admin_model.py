from config.database import db
from flask_login import UserMixin

class Admin(UserMixin, db.Model):
    __tablename__ = "Admins"

    admin_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def get_id(self):
        return str(self.admin_id)
