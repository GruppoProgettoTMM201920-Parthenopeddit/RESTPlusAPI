from app.main import db, whooshee
from app.main.model.device_token import DeviceToken
from app.main.model.user import User
from app.main.util.UniparthenopeAPI.requests import login_request
from app.main.util.extract_resource import extract_resource


def login(token, user_id):
    result, result_code, dev_fag = login_request(token)
    if result_code == 200:
        if not dev_fag and not result['user']['grpDes'] == "Studenti" and not result['user']['grpId'] == 6:
            return {
               'status': 'error',
               'message': 'not a student'
                   }, 499

        user = User.query.filter(User.id == user_id).first()
        if not user:
            new_user = User(id=user_id)
            db.session.add(new_user)
            db.session.commit()
            whooshee.reindex()
            return new_user, 201
        else:
            return user, 200
    else:
        error = result.get('errMsg')
        response_object = {
            'status': 'error',
            'message': error if error else 'Unknown error'
        }
        return response_object, 452


def register_new_token(user, request):
    try:
        token = extract_resource(request, 'token')
    except Exception:
        return {}, 400

    device = DeviceToken.query.filter(DeviceToken.token == token).first()

    if device != None:
        if device.user != user:
            device.user = user
            db.session.commit()
            return 202
        else:
            return 200
    else:
        db.session.add(DeviceToken(token=token, user=user))
        db.session.commit()
        return 201
