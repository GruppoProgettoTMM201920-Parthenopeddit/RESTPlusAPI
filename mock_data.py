from app.main import db
from app.main.model.board import Board
from app.main.model.chat import Chat
from app.main.model.comment import Comment
from app.main.model.content import Content
from app.main.model.course import Course
from app.main.model.group import Group
from app.main.model.group_chat import GroupChat
from app.main.model.group_invite import GroupInvite
from app.main.model.group_member import GroupMember
from app.main.model.message import Message
from app.main.model.post import Post
from app.main.model.review import Review
from app.main.model.user import User
from app.main.model.users_chat import UsersChat


def populate_db():
    user1 = User(id="user1")
    db.session.add(user1)
    user2 = User(id="user2")
    db.session.add(user2)
    user3 = User(id="user3")
    db.session.add(user3)

    post1 = Post(author=user1, title="post 1 di user1", body="Ciao")
    db.session.add(post1)
    post2 = Post(author=user2, title="post 1 di user2", body="Hello world")
    db.session.add(post2)

    comment1 = Comment(author=user3, body="Test commento top level a post 1", commented_content=post1, root_content=post1)
    db.session.add(comment1)
    comment2 = Comment(author=user2, body="Test commento 2nd level a commento 11", commented_content=comment1, root_content=comment1.root_content)
    db.session.add(comment2)

    comment3 = Comment(author=user3, body="test1", commented_content=comment2, root_content=comment2.root_content)
    db.session.add(comment3)
    comment4 = Comment(author=user3, body="test2", commented_content=comment2, root_content=comment2.root_content)
    db.session.add(comment4)
    comment5 = Comment(author=user2, body="test3", commented_content=comment3, root_content=comment3.root_content)
    db.session.add(comment5)
    comment6 = Comment(author=user3, body="test4", commented_content=comment5, root_content=comment5.root_content)
    db.session.add(comment6)
    comment7 = Comment(author=user2, body="test5", commented_content=comment6, root_content=comment6.root_content)
    db.session.add(comment7)
    comment8 = Comment(author=user3, body="test6", commented_content=comment7, root_content=comment7.root_content)
    db.session.add(comment8)

    user1.liked_content.append(comment1)
    user3.liked_content.append(comment2)

    course1 = Course(name="TERMINALI MOBILI E MULTIMEDIALITA")
    db.session.add(course1)

    course1.followers.append(user2)
    course1.followers.append(user3)

    review1 = Review(author=user2, reviewed_course=course1, body="Il miglior corso di sempre", score_liking=5, score_difficulty=3)
    db.session.add(review1)
    review2 = Review(author=user3, reviewed_course=course1, body="Troppo difficile", score_liking=2, score_difficulty=5)
    db.session.add(review2)

    comment_r_1 = Comment(author=user1, body="Si, adoro android!", commented_content=review1, root_content=review1)
    db.session.add(comment_r_1)

    user1.liked_content.append(review1)

    group1 = Group(name="SCEMI_1", chat=GroupChat())
    db.session.add(group1)

    group1.members.append(GroupMember(user=user2, group=group1, is_owner=True))
    group1.members.append(GroupMember(user=user3, group=group1, is_owner=False))

    db.session.add(Post(author=user2, title="user1 cant see this", body="Nothing to see for you, user1 hahaha", posted_to_board=group1))
    db.session.add(Post(author=user2, title="user1 cant see this", body="Nothing to see for you, user1 hahaha", posted_to_board=group1))
    db.session.add(Post(author=user2, title="user1 cant see this", body="Nothing to see for you, user1 hahaha", posted_to_board=group1))
    db.session.add(Post(author=user2, title="user1 cant see this", body="Nothing to see for you, user1 hahaha", posted_to_board=group1))
    db.session.add(Post(author=user2, title="user1 cant see this", body="Nothing to see for you, user1 hahaha", posted_to_board=group1))
    db.session.add(Post(author=user2, title="user1 cant see this", body="Nothing to see for you, user1 hahaha", posted_to_board=group1))

    db.session.commit()
