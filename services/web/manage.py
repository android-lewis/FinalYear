from flask.cli import FlaskGroup
from api import create_app, db
import unittest

app = create_app("api.config.Config")
cli = FlaskGroup(app)

@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command("run")
def run():
    app.run()

@cli.command("test")
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('web/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    
    if result.wasSuccessful():
        return 0

    return 1
    
if __name__ == "__main__":
    cli()