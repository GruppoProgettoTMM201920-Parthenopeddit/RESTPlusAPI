from app.main import db
from app.main.model.user import User
from app.main.util.UniparthenopeAPI.requests import login_request


def login(token, user_id):
    def __first_login():
        new_user = User(id=user_id)

        save_changes(new_user)
        response_object = {
            'status': 'success',
            'message': 'User first login',
            'id': user_id,
            'body': result
        }
        return response_object, 201

    def __standard_login():
        response_object = {
            'status': 'success',
            'message': 'User login successful',
            'id': user_id,
            'body': result
        }
        return response_object, 200

    def __error():
        error = result.get('errMsg')
        response_object = {
            'status': 'error',
            'message': error if error else 'Unknown error'
        }
        return response_object, 401

    result, result_code = login_request(token)
    if result_code == 200:
        user = User.query.filter(User.id == user_id).first()
        if not user:
            return __first_login()
        else:
            return __standard_login()
    else:
        return __error()


def save_changes(data):
    db.session.add(data)
    db.session.commit()
