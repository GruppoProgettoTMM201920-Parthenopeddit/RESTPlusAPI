from app.main import db


def like_content(user, content):
    if content == user.liked_content.filter_by(id=content.id).first():
        user.liked_content.remove(content)
        db.session.commit()

        response_object = {
            'status': 'success',
            'message': "User removed like from post {}".format(content.id),
        }
        return response_object, 211
    elif content == user.disliked_content.filter_by(id=content.id).first():
        user.disliked_content.remove(content)
        response_object = {
            'status': 'success',
            'message': "User removed dislike and liked post {}".format(content.id),
        }
        user.liked_content.append(content)
        db.session.commit()
        return response_object, 212
    else:
        response_object = {
            'status': 'success',
            'message': "User liked post {}".format(content.id),
        }
        user.liked_content.append(content)
        db.session.commit()
        return response_object, 210


def dislike_content(user, content):
    if content == user.disliked_content.filter_by(id=content.id).first():
        user.disliked_content.remove(content)
        db.session.commit()

        response_object = {
            'status': 'success',
            'message': "User removed dislike from post {}".format(content.id),
        }
        return response_object, 211
    elif content == user.liked_content.filter_by(id=content.id).first():
        user.liked_content.remove(content)
        response_object = {
            'status': 'success',
            'message': "User removed like and disliked post {}".format(content.id),
        }
        user.disliked_content.append(content)
        db.session.commit()
        return response_object, 212
    else:
        response_object = {
            'status': 'success',
            'message': "User disliked post {}".format(content.id),
        }
        user.disliked_content.append(content)
        db.session.commit()
        return response_object, 210
