from ..database import db

class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    department = db.Column(db.String(50), nullable=False)  # manager, employee, etc.

    def __repr__(self):
        return f'<Personnel {self.full_name}>'
