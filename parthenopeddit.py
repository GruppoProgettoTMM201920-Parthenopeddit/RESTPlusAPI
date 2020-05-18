import os

from flask_migrate import Migrate

import cli
from app import blueprint
from app.main import create_app, db
from app.main.model import user, content, post, comment, review, board, course, group

app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')
app.register_blueprint(blueprint)
app.app_context().push()
migrate = Migrate(app, db)
cli.register(app)


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': user,
        'Content': content,
        'Post': post,
        'Review': review,
        'Comment': comment,
        'Board': board,
        'Course': course,
        'Group': group,
    }


if __name__ == '__main__':
    app.run()
