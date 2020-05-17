from enum import Enum

from flask_restplus import fields

from app.main.config import COMMENTS_RECURSIVE_DEPTH

user_mapping = {
    'id': fields.String(description='User id'),
    'display_name': fields.String(description='Displayed name'),
    'registered_on': fields.DateTime(description='Date and time of first login'),
}
content_mapping = {
    'id': fields.Integer(description='Content id'),
    'body': fields.String(description='Message body of the content'),
    'timestamp': fields.DateTime(description='Date and time of publication'),
    'author_id': fields.String(description='User id of the author'),
    'comments_num': fields.Integer(description='number of comments received'),
    'likes_num': fields.Integer(description='number of likes received'),
    'dislikes_num': fields.Integer(description='number of dislikes received'),
    'type': fields.String(description='Content type (Post, Comment, Review)'),
}
post_fields_mapping = {
    'title': fields.String(description='Title of the post'),
    'posted_to_board_id': fields.Integer(description='Board id this post has been published to'),
}
post_mapping = dict(content_mapping, **post_fields_mapping)
comment_fields_mapping = {
    'commented_content_id': fields.Integer(description='Id of commented content'),
}
comment_mapping = dict(content_mapping, **comment_fields_mapping)
review_fields_mapping = {
    'reviewed_course_id': fields.Integer(description='id of reviewed course'),
    'score_liking': fields.Integer(description='0 to 5 score of liking for the reviewed course'),
    'score_difficulty': fields.Integer(description='0 to 5 score of difficulty for the reviewed course'),
}
review_mapping = dict(content_mapping, **review_fields_mapping)

new_post_mapping = {
    'title': fields.String(required=True, description='Title of the post'),
    'body': fields.String(required=True, description='Message body of the post'),
    'board_id': fields.Integer(required=False, description='Board id this post has been published to. empty if visible by everyone'),
}
new_comment_mapping = {
    'body': fields.String(required=True, description='Message body of the comment'),
    'commented_content_id': fields.Integer(required=True, description='Id of commented content'),
}
new_review_mapping = {
    'body': fields.String(required=True, description='Message body of the comment'),
    'reviewed_course_id': fields.Integer(required=True, description='id of reviewed course'),
    'score_liking': fields.Integer(required=False, description='0 to 5 score of liking for the reviewed course'),
    'score_difficulty': fields.Integer(required=False,
                                       description='0 to 5 score of difficulty for the reviewed course'),
}


class ContentType(Enum):
    POST = {'map': post_mapping, 'label': 'post_{}'}
    REVIEW = {'map': review_mapping, 'label': 'comment_{}'}
    COMMENT = {'map': comment_mapping, 'label': 'review_{}'}


def get_user_model(api):
    return api.model('user', user_mapping)


def get_post_model(api):
    return api.model('post', post_mapping)


def get_comment_model(api):
    return api.model('comment', comment_mapping)


def get_review_model(api):
    return api.model('review', review_mapping)


def get_new_post_model(api):
    return api.model('new post', new_post_mapping)


def get_new_comment_model(api):
    return api.model('new comment', new_comment_mapping)


def get_new_review_model(api):
    return api.model('new review', new_review_mapping)


def get_content_with_comments_model(api, content_type, recursive_steps=COMMENTS_RECURSIVE_DEPTH):
    rec_content_mapping = content_type['map'].copy()
    if recursive_steps:
        rec_content_mapping['comments'] = fields.List(
            fields.Nested(get_content_with_comments_model(api, content_type, recursive_steps - 1)))
    return api.model(content_type['label'].format(recursive_steps), rec_content_mapping)
