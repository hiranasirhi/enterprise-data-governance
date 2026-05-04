from config.database import db

class Department(db.Model):
    __tablename__ = "Departments"

    dept_id = db.Column(db.Integer, primary_key=True)
    dept_name = db.Column(db.String(100), nullable=False, unique=True)
