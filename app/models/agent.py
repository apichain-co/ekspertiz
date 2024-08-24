from ..database import db
class Agent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    report_id = db.Column(db.Integer, db.ForeignKey('report.id'), nullable=False)

    def __repr__(self):
        return f'<Agent {self.full_name}>'