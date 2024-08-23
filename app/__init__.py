from flask import Flask
from .database import db
from .models import appointment, customer, package, report, staff  # Import models

# Import blueprints
from .routes.appointments import appointments as appointments_bp
from .routes.customers import customers as customers_bp
from .routes.reports import reports as reports_bp
from .routes.staffs import staff as staff_bp
from .routes.main import main as main_bp  # Import the main blueprint

def create_app(config_object='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_object)
    db.init_app(app)

    with app.app_context():
        db.create_all()  # Ensure all tables are created

    # Register blueprints here
    app.register_blueprint(appointments_bp)
    app.register_blueprint(customers_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(staff_bp)
    app.register_blueprint(main_bp)  # Register the main blueprint

    return app
