import errno
import os
import shutil
import unittest

from flask_migrate import init, migrate, upgrade

from mock_data import populate_db, wipe_db


def register(app):
    @app.cli.command("test")
    def test():
        """Runs the unit tests."""
        tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
        result = unittest.TextTestRunner(verbosity=2).run(tests)
        if result.wasSuccessful():
            return 0
        return 1

    @app.cli.command("resetdb")
    def resetdb():
        """Resets the database"""
        print("deleting old db")
        delete_db()
        print("Creating db")
        create_db()
        print("Populating db with mock data")
        populate_db()
        print("Done")

    @app.cli.command("deletedb")
    def deletedb():
        """Deletes the database"""
        delete_db()

    @app.cli.command("createdb")
    def createdb():
        """Creates the database"""
        create_db()

    @app.cli.command("populatedb")
    def populatedb():
        """Populates the database with mockdata"""
        populate_db()

    @app.cli.command("wipedb")
    def wipedb():
        """Wipes database clean, preserving schema"""
        wipe_db()

    def delete_db():
        def errorRemoveReadonly(func, path, exc):
            excvalue = exc[1]
            if func in (os.rmdir, os.remove) and excvalue.errno == errno.EACCES:
                # change the file to be readable,writable,executable: 0777
                os.chmod(path, os.stat.S_IRWXU | os.stat.S_IRWXG | os.stat.S_IRWXO)
                # retry
                func(path)
            else:
                raise Exception("error in removing migrations folder")
        try:
            shutil.rmtree("./migrations", ignore_errors=False, onerror=errorRemoveReadonly)
            shutil.rmtree("./whooshee", ignore_errors=False, onerror=errorRemoveReadonly)
            os.remove("flask_boilerplate_main.db")
        except:
            pass

    def create_db():
        init()
        migrate()
        upgrade()

    pass
