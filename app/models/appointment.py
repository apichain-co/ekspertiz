from ..database import db


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    reminder_sent = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Appointment {self.brand} - {self.date} {self.time}>'
