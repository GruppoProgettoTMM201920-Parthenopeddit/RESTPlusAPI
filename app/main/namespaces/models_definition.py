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

content_base_mapping = {
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
post_mapping = dict(content_base_mapping, **post_fields_mapping)

comment_fields_mapping = {
    'commented_content_id': fields.Integer(description='Id of commented content'),
    'root_content_id': fields.Integer(description='Id of root commented content'),
}
comment_mapping = dict(content_base_mapping, **comment_fields_mapping)

review_fields_mapping = {
    'reviewed_course_id': fields.Integer(description='id of reviewed course'),
    'score_liking': fields.Integer(description='0 to 5 score of liking for the reviewed course'),
    'score_difficulty': fields.Integer(description='0 to 5 score of difficulty for the reviewed course'),
}
review_mapping = dict(content_base_mapping, **review_fields_mapping)

content_full_mapping = dict(content_base_mapping, **review_fields_mapping, **post_fields_mapping, **comment_fields_mapping)

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
    'type': fields.String()
}
group_fields_mapping = {
    'created_on': fields.DateTime(description='Date on which the group has been created'),
    'members_num': fields.Integer(),
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
message_mapping = {
    'id': fields.Integer(description='Message identifier'),
    'body': fields.String(description='text of the message'),
    'timestamp': fields.DateTime(description='date and time message was sent on'),
    'sender_id': fields.String(),
    'receiver_id': fields.Integer(),
}
new_message_mapping = {
    'body': fields.String(description='text of the message'),
}
new_device_token_mapping = {
    'token': fields.String(description='Device token')
}

like_dislike_score_mapping = {
    'likes_num': fields.Integer(description='number of likes received'),
    'dislikes_num': fields.Integer(description='number of dislikes received'),
}

course_fields_mapping = {
    'followers_num': fields.Integer(),
    'reviews_count': fields.Integer(),
    'average_difficulty_score': fields.Float,
    'average_liking_score': fields.Float
}
course_mapping = dict(board_mapping, **course_fields_mapping)

user_chat_mapping = {
    'id': fields.Integer(),
    'of_user_id': fields.String(),
    'last_opened_on': fields.DateTime(),
    'other_user_chat_id': fields.Integer(),
}

new_name_mapping = {
    'display_name': fields.String()
}


def get_like_dislike_score_model(api):
    return api.model('like and dislike score', like_dislike_score_mapping)


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


def get_board_model(api):
    return api.model('board', board_mapping)


def get_course_model(api):
    return api.model('course', course_mapping)


def get_post_model(api):
    post_model = post_mapping.copy()
    post_model['author'] = fields.Nested(get_simple_user_model(api))
    post_model['posted_to_board'] = fields.Nested(get_board_model(api))
    return api.model('post', post_model)


def get_comment_model(api):
    comment_model = comment_mapping.copy()
    comment_model['author'] = fields.Nested(get_simple_user_model(api))
    return api.model('comment', comment_model)


def get_review_model(api):
    review_model = review_mapping.copy()
    review_model['author'] = fields.Nested(get_simple_user_model(api))
    review_model['reviewed_course']: fields.Nested(get_course_model(api))
    return api.model('review', review_model)


def __get_recursive_comments_model(api, recursive_steps=COMMENTS_RECURSIVE_DEPTH-1):
    comment_model = comment_mapping.copy()
    comment_model['author'] = fields.Nested(get_simple_user_model(api))

    if recursive_steps:
        comment_model['comments'] = fields.List(
            fields.Nested(
                __get_recursive_comments_model(api, recursive_steps - 1)
            )
        )
    return api.model("content_comment_{}".format(recursive_steps), comment_model)


def get_post_with_comments_model(api, recursive_steps=COMMENTS_RECURSIVE_DEPTH):
    post_model = post_mapping.copy()
    post_model['author'] = fields.Nested(get_simple_user_model(api))
    post_model['posted_to_board'] = fields.Nested(get_board_model(api))

    if recursive_steps:
        post_model['comments'] = fields.List(
            fields.Nested(
                __get_recursive_comments_model(api, recursive_steps - 1)
            )
        )

    model_label = "post with comments"
    return api.model(model_label, post_model)


def get_comment_with_comments_model(api, recursive_steps=COMMENTS_RECURSIVE_DEPTH):
    comment_model = comment_mapping.copy()
    comment_model['author'] = fields.Nested(get_simple_user_model(api))

    if recursive_steps:
        comment_model['comments'] = fields.List(
            fields.Nested(
                __get_recursive_comments_model(api, recursive_steps - 1)
            )
        )

    model_label = "comment with comments"
    return api.model(model_label, comment_model)


def get_review_with_comments_model(api, recursive_steps=COMMENTS_RECURSIVE_DEPTH):
    review_model = review_mapping.copy()
    review_model['author'] = fields.Nested(get_simple_user_model(api))
    review_model['reviewed_course']: fields.Nested(get_course_model(api))

    if recursive_steps:
        review_model['comments'] = fields.List(
            fields.Nested(
                __get_recursive_comments_model(api, recursive_steps - 1)
            )
        )

    model_label = "review with comments"
    return api.model(model_label, review_model)


def get_page_selection_model(api):
    return api.model('page selection', page_selection_mapping)


def get_group_model(api):
    return api.model('group', group_mapping)


def get_user_group_model(api):
    group_member_model = group_member_mapping.copy()
    group_member_model['user'] = fields.Nested(get_simple_user_model(api))
    group_member_model['group'] = fields.Nested(get_group_model(api))
    return api.model('user group membership', group_member_model)


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
        'inviter_id': fields.String(),
        'invited_id': fields.String(),
        'group_id': fields.Integer(),
        'timestamp': fields.DateTime(),
    }
    return api.model('group invite', group_invite_model)


def get_answer_model(api):
    return api.model('answer', {'answer': fields.Boolean(description="yes or no")})


def __get_simple_message_model(api):
    message_model = message_mapping.copy()
    message_model['sender_user'] = fields.Nested(get_simple_user_model(api))
    return api.model('replied_message', message_model)


def get_message_model(api):
    message_model = message_mapping.copy()
    message_model['sender_user'] = fields.Nested(get_simple_user_model(api))
    return api.model('message', message_model)


def get_new_message_model(api):
    return api.model('new message', new_message_mapping)


def get_new_device_token_model(api):
    return api.model('new device token', new_device_token_mapping)


def get_user_chat_model(api, get_other_chat=False):
    user_chat_model = user_chat_mapping.copy()
    user_chat_model['of_user'] = fields.Nested(get_simple_user_model(api))
    if get_other_chat == True:
        user_chat_model['other_user_chat'] = fields.Nested(get_user_chat_model(api), get_other_chat=False)
        user_chat_model['last_message'] = fields.Nested(get_message_model(api))
        return api.model('User chat with user', user_chat_model)
    else:
        return api.model('Other user chat with user', user_chat_model)


def get_user_chat_model_with_log(api):
    user_chat_model = user_chat_mapping.copy()
    user_chat_model['of_user'] = fields.Nested(get_simple_user_model(api))
    user_chat_model['other_user_chat'] = fields.Nested(get_user_chat_model(api), get_other_chat=False)
    user_chat_model['chat_log'] = fields.List(fields.Nested(get_message_model(api)))
    return api.model('User chat log with user', user_chat_model)

def get_new_display_name_model(api):
    return api.model('set display name', new_name_mapping)
