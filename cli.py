import os
import unittest

from app.main import db
from app.main.model.comment import Comment
from app.main.model.post import Post
from app.main.model.user import User


def register(app):
    @app.cli.command("test")
    def test():
        """Runs the unit tests."""
        tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
        result = unittest.TextTestRunner(verbosity=2).run(tests)
        if result.wasSuccessful():
            return 0
        return 1

    @app.cli.command("mockdb")
    def mock_db():
        """Mocks the database"""
        createdb()
        populatedb()

    @app.cli.command("createdb")
    def createdb():
        """Deletes the database"""
        os.system("flask db init")
        os.system("flask db migrate")
        os.system("flask db upgrade")

    @app.cli.command("populatedb")
    def populatedb():
        """Populates the database with mockdata"""
        u1 = User(id="user1")
        db.session.add(u1)
        u2 = User(id="user2")
        db.session.add(u2)
        u3 = User(id="user3")
        db.session.add(u3)

        p1 = Post(id=1, author_id="user1", title="post 1 of user1", body="Hello")
        db.session.add(p1)
        p2 = Post(id=2, author_id="user2", title="post 1 of user2", body="Hello world")
        db.session.add(p2)

        c1 = Comment(id=3, author_id="user3", body="Hi new guy", commented_content_id="1")
        db.session.add(c1)
        c2 = Comment(id=4, author_id="user2", body="He is not new, dumbass", commented_content_id="3")
        db.session.add(c2)

        db.session.commit()

    pass
