from app.main import db, whooshee
from app.main.model.board import Board
from app.main.model.post import Post
from app.main.namespaces.content_accessibility import is_post_accessible
from app.main.namespaces.like_dislike_framework import like_content, dislike_content
from app.main.util.extract_resource import extract_resource
from app.main.model.course import Course
from app.main.namespaces.groups.group_decorator import check_group_accessibility


def search_post(user, searched_post_title):
    joined_groups_sq = user.joined_groups.subquery('joined_groups', True)

    return Post.query.join(
        joined_groups_sq,
        Post.posted_to_board_id == joined_groups_sq.c.group_id
    ).union(
        Post.query.join(
            Course,
            Post.posted_to_board_id == Course.id
        ).with_entities(Post)
    ).union(
        Post.query.filter(
            Post.posted_to_board_id == None
        )
    ).whooshee_search(searched_post_title).limit(20).all(), 200


def save_new_post(user, request):
    try:
        title = extract_resource(request, 'title')
        body = extract_resource(request, 'body')
    except:
        return {}, 400

    try:
        board_id = int(extract_resource(request, 'board_id'))
    except:
        board_id = None

    if board_id != None and board_id != 0:
        board = Board.query.filter(Board.id == board_id).first_or_404()
        if not board:
            response_object = {
                'status': 'error',
                'message': 'invalid board_id supplied',
            }
            return response_object, 300
        else:
            if board.type == 'group':
                accessible, is_owner, group = check_group_accessibility(user, board_id)
                if not accessible:
                    response_object = {
                        'status': 'error',
                        'message': 'Cant post to private group',
                    }
                    return response_object, 401
    else:
        board_id = None

    author_id = user.id
    new_post = Post(author_id=author_id, title=title, body=body, posted_to_board_id=board_id)

    db.session.add(new_post)
    db.session.commit()
    whooshee.reindex()

    return new_post, 201


def get_post_by_id(user, post_id):
    accessible, post = is_post_accessible(user, post_id)
    if not accessible:
        response_object = {
            'status': 'error',
            'message': "Post is private",
        }
        return response_object, 401

    return post, 200


def like_post_by_id(user, post_id):
    accessible, post = is_post_accessible(user, post_id)
    if not accessible:
        response_object = {
            'status': 'error',
            'message': "Post is private",
        }
        return response_object, 401

    return like_content(user, post)


def dislike_post_by_id(user, post_id):
    accessible, post = is_post_accessible(user, post_id)
    if not accessible:
        response_object = {
            'status': 'error',
            'message': "Post is private",
        }
        return response_object, 401

    return dislike_content(user, post)
