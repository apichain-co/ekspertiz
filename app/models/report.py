from datetime import datetime
from ..database import db


class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    inspection_date = db.Column(db.Date, nullable=False)
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
    vehicle_owner = db.relationship('VehicleOwner', uselist=False, backref='report', cascade="all, delete-orphan")
    agent = db.relationship('Agent', uselist=False, backref='report', cascade="all, delete-orphan")
    registration_document_seen = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f'<Report {self.vehicle_plate} - {self.inspection_date}>'
