from App.database import db

class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    competition_id = db.Column(db.Integer, db.ForeignKey('competition.id'), nullable=False)
    student_name = db.Column(db.String(120), nullable=False)
    score = db.Column(db.Float, nullable=False)
    rank = db.Column(db.Integer, nullable=False)
