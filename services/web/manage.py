from flask.cli import FlaskGroup
from api import create_app, db

app = create_app()
cli = FlaskGroup(app)

@cli.command("create_db")
def create_db():
    with app.app_context():
        db.drop_all()
        db.create_all()
        db.session.commit()

@cli.command("run")
def run():
    app.run()

@cli.command("test")
def test():
    return None

if __name__ == "__main__":
    cli()