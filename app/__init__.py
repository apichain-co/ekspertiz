from flask import Flask
from .database import db, migrate
from .models import appointment, customer, package, report, staff, branch, company
import logging
from logging.handlers import RotatingFileHandler
from .services.commands import register_commands
from .services.expertise_initializer import ExpertiseInitializer
from .services.package_initializer import create_standard_package


# Import blueprints
from .routes.appointments import appointments as appointments_bp
from .routes.customers import customers as customers_bp
from .routes.reports import reports as reports_bp
from .routes.staffs import staff as staff_bp
from .routes.main import main as main_bp
from .routes.branches import branches as branches_bp
from .routes.companies import companies as companies_bp
from .routes.errors import errors as errors_bp
from .routes.packages import packages as packages_bp



def create_app(config_object='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_object)

    if not app.debug:
        file_handler = RotatingFileHandler('logs/error.log', maxBytes=10240, backupCount=10)
        file_handler.setLevel(logging.ERROR)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s [in %(pathname)s:%(lineno)d]')
        file_handler.setFormatter(formatter)
        app.logger.addHandler(file_handler)

    db.init_app(app)

    migrate.init_app(app, db)

    with app.app_context():
        db.create_all()
        ExpertiseInitializer.initialize_expertise_reports()  # Initialize expertise reports
        create_standard_package()
        # print_package_reports("Standard Package")



    register_commands(app)

    # Register blueprints here
    app.register_blueprint(packages_bp)
    app.register_blueprint(errors_bp)
    app.register_blueprint(branches_bp)
    app.register_blueprint(companies_bp)
    app.register_blueprint(appointments_bp)
    app.register_blueprint(customers_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(staff_bp)
    app.register_blueprint(main_bp)

    return app
