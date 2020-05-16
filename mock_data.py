from app.main import db
from app.main.model.user import User
from app.main.model.content import Content
from app.main.model.comment import Comment
from app.main.model.post import Post
from app.main.model.review import Review
from app.main.model.likes import likes
from app.main.model.dislikes import dislikes


def populate_db():
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

    u1.liked_content.append(c1)
    u3.liked_content.append(c2)

    db.session.commit()