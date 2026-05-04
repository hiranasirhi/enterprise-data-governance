from config.database import db

class DataResource(db.Model):
    __tablename__ = "Data_Resources"

    resource_id = db.Column(db.Integer, primary_key=True)
    resource_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    sensitivity_level = db.Column(db.Enum('Low', 'Medium', 'High'), nullable=False)
    data_owner_id = db.Column(db.Integer, db.ForeignKey("Users.user_id"))
