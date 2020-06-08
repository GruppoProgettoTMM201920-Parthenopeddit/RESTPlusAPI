import os

import cli
from app import blueprint
from app.main import create_app, db

app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')

app.register_blueprint(blueprint)
app.app_context().push()
cli.register(app)


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db
    }


if __name__ == '__main__':
    app.run(ssl_context=('cert.pem', 'key.pem'))
