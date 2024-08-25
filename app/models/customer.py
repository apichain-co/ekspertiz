from ..database import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    tc_tax_number = db.Column(db.String(11), nullable=True)
    email = db.Column(db.String(100))
    address = db.Column(db.String(255))
    reports = db.relationship('Report', backref='customer', lazy=True)

    def __repr__(self):
        return f'<Customer {self.full_name}>'