from app.main.model.board import Board
from app.main.model.course import Course
from app.main import db
from app.main.model.post import Post
from app.main.util.extract_resource import extract_resource
from app.main.model.review import Review


def search_course(course_name):
    if len(course_name) < 3:
        response_object = {
            'status': 'error',
            'message': 'search string is too small. need 3 characters minimum',
        }
        return response_object, 300

    return Board.query.filter(Board.type == 'course').whooshee_search(course_name).all(), 200


def get_user_groups(user):
    return user.followed_courses.all(), 200


def get_course_by_id(course_id):
    return Course.query.filter(Course.id == course_id).first_or_404(), 200


def get_course_followers(course_id):
    course = Course.query.filter(Course.id == course_id).first_or_404()

    return course.followers.all(), 200


def follow_course(user, course_id):
    course = Course.query.filter(Course.id == course_id).first_or_404()

    if course in user.followed_courses.all():
        response_object = {
            'status': 'error',
            'message': 'Already following course',
        }
        return response_object, 300

    user.followed_courses.append(course)
    db.session.commit()

    response_object = {
        'status': 'Success',
        'message': 'Now following course',
    }
    return response_object, 201


def unfollow_course(user, course_id):
    course = Course.query.filter(Course.id == course_id).first_or_404()

    if course not in user.followed_courses.all():
        response_object = {
            'status': 'error',
            'message': "Can't unfollow not followed course",
        }
        return response_object, 300

    user.followed_courses.remove(course)
    db.session.commit()

    response_object = {
        'status': 'Success',
        'message': 'Now unfollowing course',
    }
    return response_object, 201


def get_course_posts(course_id, per_page, page):
    course = Course.query.filter(Course.id == course_id).first_or_404()

    return course.posts.paginate(
        per_page=per_page,
        page=page
    ).items, 200


def publish_post_to_course(user, course_id, request):
    course = Course.query.filter(Course.id == course_id).first_or_404()

    try:
        title = extract_resource(request, 'title')
        body = extract_resource(request, 'body')
    except:
        return {}, 400

    new_post = Post(author=user, title=title, body=body, posted_to_board=course)

    db.session.add(new_post)
    db.session.commit()

    return new_post, 201


def get_course_reviews(course_id, per_page, page):
    course = Course.query.filter(Course.id == course_id).first_or_404()

    return course.reviews.paginate(
        per_page=per_page,
        page=page
    ).items, 200


def publish_review_to_course(user, course_id, request):
    course = Course.query.filter(Course.id == course_id).first_or_404()

    try:
        body = extract_resource(request, 'body')
        score_liking = extract_resource(request, 'score_liking')
        score_difficulty = extract_resource(request, 'score_difficulty')
    except:
        return {}, 400

    new_review = Review(author=user, body=body, score_liking=score_liking, score_difficulty=score_difficulty, reviewed_course=course)

    db.session.add(new_review)
    db.session.commit()

    return new_review, 201
