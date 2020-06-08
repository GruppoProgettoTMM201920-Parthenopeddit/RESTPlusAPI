from datetime import datetime

from app.main import db, whooshee
from app.main.model.comment import Comment
from app.main.model.course import Course
from app.main.model.group import Group
from app.main.model.group_chat import GroupChat
from app.main.model.group_invite import GroupInvite
from app.main.model.group_member import GroupMember
from app.main.model.likes import Likes
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
    post3 = Post(author=user3, title="post 1 di user3", body="Hello world 2")
    db.session.add(post3)

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

    like1 = Likes(user=user1, content=comment1)
    db.session.add(like1)
    like2 = Likes(user=user3, content=comment2)
    db.session.add(like2)

    course1 = Course(name="TERMINALI MOBILI E MULTIMEDIALITA")
    db.session.add(course1)

    course1.followers.append(user2)
    course1.followers.append(user3)

    course2 = Course(name="Corso di test. do not use")
    db.session.add(course2)

    course2.followers.append(user1)

    review1 = Review(author=user2, reviewed_course=course1, body="Il miglior corso di sempre", score_liking=5, score_difficulty=3)
    db.session.add(review1)
    review2 = Review(author=user3, reviewed_course=course1, body="Troppo difficile", score_liking=2, score_difficulty=5)
    db.session.add(review2)

    comment_r_1 = Comment(author=user1, body="Si, adoro android!", commented_content=review1, root_content=review1)
    db.session.add(comment_r_1)

    like3 = Likes(user=user1, content=review1)
    db.session.add(like3)

    group1 = Group(name="SCEMI_1", chat=GroupChat())
    db.session.add(group1)

    group1.members.append(GroupMember(user=user2, group=group1, is_owner=True))
    group1.members.append(GroupMember(user=user3, group=group1, is_owner=False))

    invite1 = GroupInvite(invited=user1, inviter=user2, group=group1)
    db.session.add(invite1)

    group2 = Group(name="JUST ME", chat=GroupChat())
    db.session.add(group2)

    group2.members.append(GroupMember(user=user3, group=group2, is_owner=True))

    db.session.add(Post(author=user2, title="user1 cant see this", body="Nothing to see for you, user1 hahaha", posted_to_board=group1))
    db.session.add(Post(author=user2, title="user1 cant see this", body="Nothing to see for you, user1 hahaha", posted_to_board=group1))
    db.session.add(Post(author=user2, title="user1 cant see this", body="Nothing to see for you, user1 hahaha", posted_to_board=group1))
    db.session.add(Post(author=user2, title="user1 cant see this", body="Nothing to see for you, user1 hahaha", posted_to_board=group1))
    db.session.add(Post(author=user2, title="user1 cant see this", body="Nothing to see for you, user1 hahaha", posted_to_board=group1))
    db.session.add(Post(author=user2, title="user1 cant see this", body="Nothing to see for you, user1 hahaha", posted_to_board=group1))

    like3 = Likes(user=user1, content=post3)
    db.session.add(like3)

    u1_c_2 = UsersChat(of_user=user1)
    u2_c_1 = UsersChat(of_user=user2)

    u1_c_2.other_user_chat = u2_c_1
    u2_c_1.other_user_chat = u1_c_2

    db.session.add(u1_c_2)
    db.session.add(u2_c_1)

    u1_c_3 = UsersChat(of_user=user1)
    u3_c_1 = UsersChat(of_user=user3)

    u1_c_3.other_user_chat = u3_c_1
    u3_c_1.other_user_chat = u1_c_3

    db.session.add(u1_c_3)
    db.session.add(u3_c_1)

    m1 = Message(sender_user=user1, receiver_chat=u2_c_1, body="Hello", timestamp=datetime(2020, 6, 7, 10, 10, 10))
    m2 = Message(sender_user=user2, receiver_chat=u1_c_2, body="Oh, hi", timestamp=datetime(2020, 6, 7, 10, 11, 7))
    m3 = Message(sender_user=user1, receiver_chat=u2_c_1, body="èRF,E,EèF", timestamp=datetime(2020, 6, 7, 10, 11, 9))
    m4 = Message(sender_user=user2, receiver_chat=u1_c_2, body="yes", timestamp=datetime(2020, 6, 7, 10, 11, 30))

    db.session.add(m1)
    db.session.add(m2)
    db.session.add(m3)
    db.session.add(m4)

    db.session.commit()
    whooshee.reindex()
