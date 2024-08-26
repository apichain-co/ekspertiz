from ..database import db


class Package(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    contents = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean, default=True)

    reports = db.relationship('Report', back_populates='package')  # Ensure this matches the back_populates in Report
    package_expertises = db.relationship('PackageExpertise', back_populates='package')

    def __repr__(self):
        return f'<Package {self.name}>'
