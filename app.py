from modules.access_workflow.routes.access_routes import access_bp

app.register_blueprint(access_bp, url_prefix="/access")
