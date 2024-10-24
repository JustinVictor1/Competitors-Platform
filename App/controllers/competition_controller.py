from App.models import Competition
from App.database import db
from datetime import datetime


def create_competition(name, date_str, description):
    date = datetime.strptime(date_str, '%Y-%m-%d').date()
    competition = Competition(name=name, date=date, description=description)
    db.session.add(competition)
    db.session.commit()
    return competition


def get_all_competitions():
    return Competition.query.all()


def get_competition_by_id(competition_id):
    return Competition.query.get(competition_id)
