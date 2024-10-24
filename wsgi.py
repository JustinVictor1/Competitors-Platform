from App.controllers import (create_competition, get_all_competitions,
                             get_competition_by_id, import_results_from_file,
                             get_results_by_competition)

import click
import pytest
import sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User
from App.main import create_app
from App.controllers import (create_user, get_all_users_json, get_all_users,
                             initialize)

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)




@app.cli.command('init', help='Initialize the database')
@with_appcontext
def initialize():
    db.create_all()
    print('Database tables created.')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands')


# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')


# this command will be : flask user create bob bobpass


@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())


app.cli.add_command(user_cli)  # add the group to the cli
'''
Test Commands
'''

test = AppGroup('test', help='Testing commands')


@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))


app.cli.add_command(test)

# Competition CLI group
competition_cli = AppGroup('competition', help='Competition object commands')


@competition_cli.command('create', help='Create a new competition')
@click.argument('name')
@click.argument('date')  # Date format: YYYY-MM-DD
@click.option('--description',
              default='',
              help='Description of the competition')
def create_competition_command(name, date, description):
    comp = create_competition(name, date, description)
    if comp:
        print(f'Competition "{comp.name}" created successfully.')
    else:
        print('Error creating competition.')


@competition_cli.command('list', help='List all competitions')
def list_competitions_command():
    competitions = get_all_competitions()
    for comp in competitions:
        print(
            f'ID: {comp.id}, Name: {comp.name}, Date: {comp.date}, Description: {comp.description}'
        )


# Result CLI group
result_cli = AppGroup('result', help='Result object commands')


@result_cli.command('import', help='Import results from a CSV file')
@click.argument('competition_id', type=int)
@click.argument('file_path')
def import_results_command(competition_id, file_path):
    import_results_from_file(competition_id, file_path)
    print(f'Results imported for competition ID {competition_id}.')


@result_cli.command('view', help='View results of a competition')
@click.argument('competition_id', type=int)
def view_results_command(competition_id):
    results = get_results_by_competition(competition_id)
    for result in results:
        print(
            f'Student: {result.student_name}, Score: {result.score}, Rank: {result.rank}'
        )


# Register the CLI groups
app.cli.add_command(competition_cli)
app.cli.add_command(result_cli)
