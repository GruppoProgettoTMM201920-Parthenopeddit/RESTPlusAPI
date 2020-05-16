from flask_restplus import fields
from app.main.config import COMMENTS_RECURSIVE_DEPTH, POST_RECURSIVE_DEPTH

post_mapping = {
    'id': fields.Integer(description='ID of the post'),
    'title': fields.String(description='Title of the post'),
    'body': fields.String(description='Message body of the post'),
    'timestamp': fields.DateTime(description='Date and time of publication'),
    'author_id': fields.String(description='User id of the author'),
    'comments_num': fields.Integer(description='Number of comments this post has received')
}
new_post_mapping = {
    'title': fields.String(required=True, description='Title of the post'),
    'body': fields.String(required=False, description='Message body of the post')
}
comment_mapping = {
    'id': fields.Integer(description='ID of the comment'),
    'body': fields.String(description='Message body of the comment'),
    'timestamp': fields.DateTime(description='Date and time of publication'),
    'author_id': fields.String(description='User id of the author'),
    'commented_post_id': fields.Integer(description='Id of commented post'),
    'commented_comment_id': fields.Integer(description='Id of commented comment'),
    'comments_num': fields.Integer(description='Number of comments this comment has received')
}
new_comment_mapping = {
    'body': fields.String(required=True, description='Message body of the comment')
}
user_mapping = {
    'id': fields.String(description='User id'),
    'nome_visualizzato': fields.String(description='Displayed name'),
    'registrato_il': fields.DateTime(description='Date and time of first login'),
    'posts_num': fields.Integer(description='Number of posts user is author of'),
    'comments_num': fields.Integer(description='Number of comments user is author of')
}


def get_user_model(api):
    return api.model('user', user_mapping)


def get_post_model(api):
    return api.model('post', post_mapping)


def get_post_with_comments_model(api, recursive_steps=POST_RECURSIVE_DEPTH):
    rec_post_mapping = post_mapping.copy()
    if recursive_steps:
        rec_post_mapping['comments'] = fields.List(fields.Nested(get_comment_with_comments_model(api, recursive_steps-1)))
    return api.model('post_'.format(recursive_steps), rec_post_mapping)


def get_new_post_model(api):
    return api.model('new post', new_post_mapping)


def get_comment_model(api):
    return api.model('comment', comment_mapping)


def get_comment_with_comments_model(api, recursive_steps=COMMENTS_RECURSIVE_DEPTH):
    rec_comment_mapping = comment_mapping.copy()
    if recursive_steps:
        rec_comment_mapping['comments'] = fields.List(fields.Nested(get_comment_with_comments_model(api, recursive_steps-1)))
    return api.model('comment_{}'.format(recursive_steps), rec_comment_mapping)


def get_new_comment_model(api):
    return api.model('new comment', new_comment_mapping)
