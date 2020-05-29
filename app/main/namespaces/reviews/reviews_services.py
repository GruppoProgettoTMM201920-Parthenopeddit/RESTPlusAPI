from app.main import db
from app.main.model.course import Course
from app.main.model.review import Review
from app.main.model.user import User
from app.main.namespaces.like_dislike_framework import like_content, dislike_content
from app.main.util.extract_resource import extract_resource


def save_new_review(user, request):
    try:
        body = extract_resource(request, 'body')
        reviewed_course_id = int(extract_resource(request, 'reviewed_course_id'))
        score_liking = int(extract_resource(request, 'score_liking'))
        score_difficulty = int(extract_resource(request, 'score_difficulty'))
    except:
        return {}, 400

    if reviewed_course_id is None:
        response_object = {
            'status': 'error',
            'message': 'invalid reviewed_course_id supplied',
        }
        return response_object, 300

    course = Course.query.filter(Course.id == reviewed_course_id).first_or_404()
    if not course:
        response_object = {
            'status': 'error',
            'message': 'invalid reviewed_course_id supplied',
        }
        return response_object, 300

    if score_liking > 5 or score_liking < 0 or score_difficulty > 5 or score_difficulty < 0:
        response_object = {
            'status': 'error',
            'message': 'invalid score supplied. must be a value between 0 and 5',
        }
        return response_object, 300

    new_review = Review(author=user, body=body, score_liking=score_liking, score_difficulty=score_difficulty, reviewed_course_id=reviewed_course_id)
    db.session.add(new_review)
    db.session.commit()

    return new_review, 201


def get_review_by_id(review_id):
    review = Review.query.filter(Review.id == review_id).first_or_404()
    return review, 200


def like_review_by_id(user, review_id):
    review = Review.query.filter(Review.id == review_id).first_or_404()
    return like_content(user, review)


def dislike_review_by_id(user, review_id):
    review = Review.query.filter(Review.id == review_id).first_or_404()
    return dislike_content(user, review)
