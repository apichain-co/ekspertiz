from ..database import db


class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    department = db.Column(db.String(50), nullable=False)  # e.g., "IT", "Sales", etc.
    role = db.Column(db.String(50), nullable=False)  # e.g., "Officer", "Manager", "Employee"
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'), nullable=False)

    def __repr__(self):
        return f'<Staff {self.full_name} - {self.role}>'