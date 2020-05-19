from app.main.model.comment import Comment
from app.main.model.content import Content
from app.main.model.group import Group
from app.main.model.post import Post
from app.main.model.user import User


def __is_post_accessible(user, post):
    if post.posted_to_board_id is not None:
        board = post.posted_to_board
        if board.type == 'group':
            group = board
            if group != user.joined_groups.filter(Group.id == group.id).first():
                return False
    return True


def __is_comment_accessible(user, comment):
    root_content = comment.root_content

    if root_content.type == 'post':
        post = root_content
        return __is_post_accessible(user, post)
    return True


def is_comment_accessible(user_id, comment_id):
    comment = Comment.query.filter(Comment.id == comment_id).first_or_404()
    user = User.query.filter(User.id == user_id).first_or_404()

    return __is_comment_accessible, user, comment


def is_post_accessible(user_id, post_id):
    post = Post.query.filter(Post.id == post_id).first_or_404()
    user = User.query.filter(User.id == user_id).first_or_404()

    return __is_post_accessible(user, post), user, post


def is_content_accessible(user_id, content_id):
    content = Content.query.filter(Content.id == content_id).first_or_404()
    user = User.query.filter(User.id == user_id).first_or_404()

    if content.type == 'post':
        return __is_post_accessible(user, content), user, content
    else:
        if content.type == 'comment':
            return __is_comment_accessible(user, content), user, content
    return True, user, content
