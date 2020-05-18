from app.main import db
from app.main.model.course import Course
from app.main.model.review import Review
from app.main.model.user import User


def save_new_review(token, user_id, payload):
    reviewed_course_id = payload['reviewed_course_id']
    if reviewed_course_id is None:
        response_object = {
            'status': 'error',
            'message': 'no reviewed_course_id supplied',
        }
        return response_object, 300

    course = Course.query.filter(Course.id == reviewed_course_id).first_or_404()
    if not course:
        response_object = {
            'status': 'error',
            'message': 'invalid reviewed_course_id supplied',
        }
        return response_object, 300

    author_id = user_id
    body = payload['body']
    score_liking = payload['score_liking']
    score_difficulty = payload['score_difficulty']
    new_review = Review(author_id=author_id, body=body, score_liking=score_liking, score_difficulty=score_difficulty, reviewed_course_id=reviewed_course_id)
    save_changes(new_review)

    response_object = {
        'status': 'success',
        'message': 'Review published successfully',
        'id': new_review.id
    }
    return response_object, 200


def get_review_by_id(token, user_id, review_id):
    review = Review.query.filter(Review.id == review_id).first_or_404()
    user = User.query.filter(User.id == user_id).first_or_404()

    return review, 200


def save_changes(data):
    db.session.add(data)
    db.session.commit()
