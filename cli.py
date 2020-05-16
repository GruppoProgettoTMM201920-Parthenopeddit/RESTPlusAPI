import unittest


def register(app):
    @app.cli.command("test")
    def test():
        """Runs the unit tests."""
        tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
        result = unittest.TextTestRunner(verbosity=2).run(tests)
        if result.wasSuccessful():
            return 0
        return 1

    pass
