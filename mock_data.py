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


def populate_db():
    user1 = User(id="user1")
    db.session.add(user1)
    user2 = User(id="user2")
    db.session.add(user2)
    user3 = User(id="user3")
    db.session.add(user3)

    db.session.commit()

    post1 = Post(author=user1, title="post 1 di user1", body="Ciao")
    db.session.add(post1)
    post2 = Post(author=user2, title="post 1 di user2", body="Hello world")
    db.session.add(post2)

    db.session.commit()

    comment1 = Comment(author=user3, body="Ciao, sei nuovo?", commented_content=post1)
    db.session.add(comment1)
    comment2 = Comment(author=user2, body="Mi sembra ovvio", commented_content=comment1)
    db.session.add(comment2)

    db.session.commit()

    user1.liked_content.append(comment1)
    user3.liked_content.append(comment2)

    db.session.commit()

    course1 = Course(name="TERMINALI MOBILI E MULTIMEDIALITA")
    db.session.add(course1)

    db.session.commit()

    review1 = Review(author=user2, reviewed_course=course1, body="Il miglior corso di sempre", score_liking=5, score_difficulty=3)
    db.session.add(review1)

    review2 = Review(author=user3, reviewed_course=course1, body="Troppo difficile", score_liking=2, score_difficulty=5)
    db.session.add(review2)

    db.session.commit()
