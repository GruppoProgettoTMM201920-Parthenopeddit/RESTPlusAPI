from app.main.model.comment import Comment
from app.main.model.content import Content
from app.main.model.group import Group
from app.main.model.post import Post


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


def is_comment_accessible(user, comment_id):
    comment = Comment.query.filter(Comment.id == comment_id).first_or_404()

    return __is_comment_accessible(user, comment), comment


def is_post_accessible(user, post_id):
    post = Post.query.filter(Post.id == post_id).first_or_404()
    return __is_post_accessible(user, post), post


def is_content_accessible(user, content_id):
    content = Content.query.filter(Content.id == content_id).first_or_404()

    if content.type == 'post':
        return __is_post_accessible(user, content), content
    elif content.type == 'comment':
        return __is_comment_accessible(user, content), content
    else:
        return True, content
