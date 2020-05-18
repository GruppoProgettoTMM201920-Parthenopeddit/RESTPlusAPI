from sqlalchemy import text

from parthenopeddit import app
from app.main import db
from app.main.model.user import User
from app.main.model.content import Content
from app.main.model.comment import Comment
from app.main.model.post import Post
from app.main.model.review import Review
from app.main.model.likes import likes
from app.main.model.dislikes import dislikes
from app.main.model.board import Board
from app.main.model.group import Group
from app.main.model.course import Course

if __name__ == '__main__':
    u1 = User.query.filter_by(id="user1").first_or_404()
    print(u1)

    u2 = User.query.filter_by(id="user2").first_or_404()
    print(u2)

    u3 = User.query.filter_by(id="user3").first_or_404()
    print(u3)

    print(type(u2.boards))
    print(u2.boards.with_entities(Board.id).all())

    print(

    )

    # db.session.query(Post).join(u2.boards)

    # u2_boards = u2.boards.all()
    # print(u2_boards)
    #
    # u2_visible_posts = Post.query.filter(Post.posted_to_board_id == None).all()
    #
    # for board in u2_boards:
    #     u2_visible_posts.append(board.posts.all())
    #
    # print(u2_visible_posts)
