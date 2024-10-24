from App.models import Result
from App.database import db


def add_result(competition_id, student_name, score, rank):
    result = Result(competition_id=competition_id,
                    student_name=student_name,
                    score=score,
                    rank=rank)
    db.session.add(result)
    db.session.commit()
    return result


def import_results_from_file(competition_id, file_path):

    import csv
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            add_result(competition_id=competition_id,
                       student_name=row['student_name'],
                       score=float(row['score']),
                       rank=int(row['rank']))


def get_results_by_competition(competition_id):
    return Result.query.filter_by(competition_id=competition_id).all()
