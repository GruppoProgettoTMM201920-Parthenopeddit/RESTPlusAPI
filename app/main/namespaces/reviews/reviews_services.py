from app.main import db
from app.main.model.course import Course
from app.main.model.review import Review
from app.main.model.user import User
from app.main.namespaces.like_dislike_framework import like_content, dislike_content


def save_new_review(user, payload):
    reviewed_course_id = payload['reviewed_course_id']
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

    author_id = user.id
    body = payload['body']
    score_liking = payload['score_liking']
    score_difficulty = payload['score_difficulty']
    new_review = Review(author_id=author_id, body=body, score_liking=score_liking, score_difficulty=score_difficulty, reviewed_course_id=reviewed_course_id)
    db.session.add(new_review)
    db.session.commit()

    return new_review, 201


def get_review_by_id(user, review_id):
    review = Review.query.filter(Review.id == review_id).first_or_404()
    return review, 200


def like_review_by_id(user, review_id):
    comment = Review.query.filter(Review.id == review_id).first_or_404()
    return like_content(user, comment)


def dislike_review_by_id(user, review_id):
    comment = Review.query.filter(Review.id == review_id).first_or_404()
    return dislike_content(user, comment)
