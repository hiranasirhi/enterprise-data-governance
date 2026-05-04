class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://govuser:govpass123@localhost/enterprise_governance"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "your-secret-key"
    
