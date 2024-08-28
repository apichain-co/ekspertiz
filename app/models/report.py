from datetime import datetime
from ..database import db


class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    inspection_date = db.Column(db.Date, nullable=True)
    vehicle_plate = db.Column(db.String(10), nullable=False)
    chassis_number = db.Column(db.String(17), nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    model_year = db.Column(db.Integer, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    package_id = db.Column(db.Integer, db.ForeignKey('package.id'), nullable=False)
    operation = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)
    registration_document_seen = db.Column(db.Boolean, nullable=False)

    # Relationships
    customer = db.relationship('Customer', back_populates='reports', overlaps="customer_reports,customer")
    package = db.relationship('Package', back_populates='reports')
    staff = db.relationship('Staff', back_populates='reports_created', overlaps="staff_reports,staff")


    def __repr__(self):
        return f'<Report {self.vehicle_plate} - {self.inspection_date}>'
