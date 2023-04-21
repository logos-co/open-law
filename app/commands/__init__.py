from flask import Flask
from app import models as m
from app import db, forms
from app import schema as s


def init(app: Flask):

    # flask cli context setup
    @app.shell_context_processor
    def get_context():
        """Objects exposed here will be automatically available from the shell."""
        return dict(app=app, db=db, m=m, f=forms, s=s)

    if app.config["ENV"] != "production":

        @app.cli.command()
        def db_populate():
            """Fill DB by dummy data."""
            from tests.db.create_dummy_data import create_dummy_data

            create_dummy_data()
            print("Dummy data added")

    @app.cli.command("create-admin")
    def create_admin():
        """Create super admin account"""
        if m.User.query.filter_by(username=app.config["ADMIN_USERNAME"]).first():
            print(
                f"User with username: [{app.config['ADMIN_USERNAME']}] already exists"
            )
            return
        m.User(
            username=app.config["ADMIN_USERNAME"],
            password=app.config["ADMIN_PASSWORD"],
        ).save()
        print("admin created")
