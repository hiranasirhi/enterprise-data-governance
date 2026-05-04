from config.database import db

class User(db.Model):
    __tablename__ = "Users"

    user_id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    dept_id = db.Column(db.Integer, db.ForeignKey("Departments.dept_id"))
    is_blocked = db.Column(db.Boolean, default=False)
    blocked_reason = db.Column(db.Text)
    blocked_at = db.Column(db.DateTime, nullable=True)
