from enum import Enum

from flask_restplus import fields

from config import COMMENTS_RECURSIVE_DEPTH

simple_user_mapping = {
    'id': fields.String(description='User id'),
    'display_name': fields.String(description='Displayed name'),
    'registered_on': fields.DateTime(description='Date and time of first login'),
}
extra_user_mapping = {
    # TODO map all user fields
}
complete_user_mapping = dict(simple_user_mapping, **extra_user_mapping)

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
page_selection_mapping = {
    'page': fields.Integer(),
    'per_page': fields.Integer(),
}

board_mapping = {
    'id': fields.Integer(description='ID of the board'),
    'name': fields.String(description='Name descriptor'),
}
group_fields_mapping = {
    'created_on': fields.DateTime(description='Date on which the group has been created'),
}
group_mapping = dict(board_mapping, **group_fields_mapping)
group_member_mapping = {
    'user_id': fields.String(description='Id of the member user'),
    'group_id': fields.Integer(description='Id of the group user if member of'),
    'join_date': fields.DateTime(description='Date on which the user joined the group'),
    'last_chat_read': fields.DateTime(description='Date on which the user last opened the chat'),
    'is_owner': fields.Boolean(description='Flag describing group ownership'),
}
new_group_mapping = {
    'group_name': fields.String(required=True, description='Name descriptor')
}

class ContentType(Enum):
    POST = 'post'
    REVIEW = 'review'
    COMMENT = 'comment'

    def getMap(self):
        switcher = {
            self.POST: post_mapping,
            self.REVIEW: review_mapping,
            self.COMMENT: comment_mapping,
        }
        return switcher.get(self)

    def getLabel(self):
        switcher = {
            self.POST: 'post',
            self.REVIEW: 'review',
            self.COMMENT: 'comment',
        }
        return switcher.get(self)


def get_complete_user_model(api):
    return api.model('user', complete_user_mapping)


def get_simple_user_model(api):
    return api.model('user (simplified)', simple_user_mapping)


def get_new_post_model(api):
    return api.model('new post', new_post_mapping)


def get_new_comment_model(api):
    return api.model('new comment', new_comment_mapping)


def get_new_review_model(api):
    return api.model('new review', new_review_mapping)


def get_content_model(api, content_type):
    content_model = content_type.getMap().copy()
    content_model['author'] = fields.Nested(get_simple_user_model(api))
    return api.model(content_type.getLabel(), content_model)


def __get_recursive_comments_model(api, recursive_steps=COMMENTS_RECURSIVE_DEPTH-1):
    comments_mapping = ContentType.COMMENT.getMap().copy()
    if recursive_steps:
        comments_mapping['comments'] = fields.List(
            fields.Nested(
                __get_recursive_comments_model(api, recursive_steps - 1)
            )
        )
    return api.model("content_comment_{}".format(recursive_steps), comments_mapping)


def get_content_with_comments_model(api, content_type, recursive_steps=COMMENTS_RECURSIVE_DEPTH):
    rec_content_mapping = content_type.getMap().copy()
    rec_content_mapping['author'] = fields.Nested(get_simple_user_model(api))
    if recursive_steps:
        rec_content_mapping['comments'] = fields.List(
            fields.Nested(
                __get_recursive_comments_model(api, recursive_steps - 1)
            )
        )
    model_label = "{}_with_comments".format(content_type.getLabel())
    return api.model(model_label, rec_content_mapping)


def get_page_selection_model(api):
    return api.model('page selection', page_selection_mapping)


def get_group_model(api):
    return api.model('group', group_mapping)


def get_user_group_model(api):
    group_member_model = group_member_mapping.copy()
    group_member_model['group'] = fields.Nested(get_group_model(api))
    return api.model('user group', group_member_model)


def get_users_id_list(api):
    users_id_list_model = {
        'users_list': fields.List(fields.String(description='id of invited user'))
    }
    return api.model('users id list', users_id_list_model)


def get_new_group_model(api):
    new_group_model = new_group_mapping.copy()
    new_group_model['invited_members'] = fields.List(fields.String(description='id of invited user'))
    return api.model('new group', new_group_model)


def get_group_invite_model(api):
    group_invite_model = {
        'inviter': fields.Nested(get_simple_user_model(api)),
        'invited': fields.Nested(get_simple_user_model(api)),
        'group': fields.Nested(get_group_model(api)),
        'timestamp': fields.DateTime,
    }
    return api.model('group invite', group_invite_model)


def get_answer_model(api):
    return api.model('answer', {'answer': fields.Boolean(description="yes or no")})
