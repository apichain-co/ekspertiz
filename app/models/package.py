from ..database import db

class Package(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    contents = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean, default=True)
    reports = db.relationship('Report', backref='package', lazy=True)

    def __repr__(self):
        return f'<Package {self.name}>'
