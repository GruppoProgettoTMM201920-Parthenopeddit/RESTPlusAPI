from app.main import db
from app.main.model.comment import Comment
from app.main.model.content import Content
from app.main.model.user import User


def save_new_comment(token, user_id, payload):
    commented_content_id = payload['commented_content_id']
    if commented_content_id is None:
        response_object = {
            'status': 'error',
            'message': 'no commented_content_id supplied',
        }
        return response_object, 300

    content = Content.query.filter(Content.id == commented_content_id).first_or_404()
    if not content:
        response_object = {
            'status': 'error',
            'message': 'invalid commented_content_id supplied',
        }
        return response_object, 300

    author_id = user_id
    body = payload['body']
    new_comment = Comment(author_id=author_id, body=body, commented_content_id=commented_content_id)
    save_changes(new_comment)

    response_object = {
        'status': 'success',
        'message': 'Comment published successfully',
        'id': new_comment.id
    }
    return response_object, 200


def get_comment_by_id(token, user_id, comment_id):
    comment = Comment.query.filter(Comment.id == comment_id).first_or_404()
    user = User.query.filter(User.id == user_id).first_or_404()

    print(comment)

    commented_content = comment.commented_content
    print(commented_content)

    print(commented_content.type)
    if commented_content.type == 'post':
        post = commented_content
        print(post.posted_to_board_id)
        if post.posted_to_board_id is not None:
            response_object = {
                'status': 'error',
                'message': "Post is private",
            }
            return response_object, 401

    return comment, 200


def save_changes(data):
    db.session.add(data)
    db.session.commit()
