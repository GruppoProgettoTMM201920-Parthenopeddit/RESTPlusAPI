from sqlalchemy.orm.collections import InstrumentedList

from app.main import db
from app.main.model.comment import Comment
from app.main.model.post import Post


def get_comment(token, user_id, comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()
    if comment:
        return comment, 200
    else:
        response_object = {
            'status': 'error',
            'message': 'No comment with given ID',
        }
        return response_object, 404


def save_new_comment(token, user_id, data, commented_id, comment_what):
    if 'body' not in data:
        response_object = {
            'status': 'error',
            'message': 'Invalid payload'
        }
        return response_object, 300

    if comment_what == "post":
        new_comment = Comment(author_id=user_id, body=data['body'], commented_post_id=commented_id)
    else:
        if comment_what == "comment":
            new_comment = Comment(author_id=user_id, body=data['body'], commented_comment_id=commented_id)
        else:
            response_object = {
                'status': 'error',
                'message': 'Internal Server Error'
            }
            return response_object, 500

    save_changes(new_comment)

    response_object = {
        'status': 'success',
        'message': 'Comment published successfully',
        'id': new_comment.id
    }
    return response_object, 200


def get_post_comments(token, user_id, post_id):
    post = Post.query.filter_by(id=post_id).first()
    if post:
        comments = post.comments.all()
        if comments:
            return comments, 200
        else:
            response_object = {
                'status': 'error',
                'message': 'Internal Server Error',
            }
            return response_object, 500

    else:
        response_object = {
            'status': 'error',
            'message': 'No post with given ID',
        }
        return response_object, 404


def get_comment_comments(token, user_id, comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()
    if comment:
        comments = comment.comments.all()
        if comments:
            if comments.__len__() > 0:
                return comments, 200
            else:
                response_object = {
                    'status': 'error',
                    'message': 'No comments for selected comment',
                }
                return response_object, 404
        else:
            response_object = {
                'status': 'error',
                'message': 'Internal Server Error',
            }
            return response_object, 500

    else:
        response_object = {
            'status': 'error',
            'message': 'No comment with given ID',
        }
        return response_object, 404


def save_changes(data):
    db.session.add(data)
    db.session.commit()
