from App.database import db


class Competition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(255))
    results = db.relationship('Result', backref='competition', lazy=True)
