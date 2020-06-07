from app.main import db
from app.main.model.dislikes import Dislikes
from app.main.model.likes import Likes


def like_content(user, content):
    like = Likes.query.filter(Likes.user_id == user.id, Likes.content_id == content.id).first()

    if like != None:
        db.session.delete(like)
        db.session.commit()

        return content, 211
    else:
        db.session.add(Likes(user=user, content=content))
        db.session.commit()

        dislike = Dislikes.query.filter(Dislikes.user_id == user.id, Dislikes.content_id == content.id).first()
        if dislike != None:
            db.session.delete(dislike)
            db.session.commit()

            return content, 212

        return content, 210


def dislike_content(user, content):
    dislike = Dislikes.query.filter(Dislikes.user_id == user.id, Dislikes.content_id == content.id).first()

    if dislike != None:
        db.session.delete(dislike)
        db.session.commit()

        return content, 211
    else:
        db.session.add(Dislikes(user=user, content=content))
        db.session.commit()

        like = Likes.query.filter(Likes.user_id == user.id, Likes.content_id == content.id).first()
        if like != None:
            db.session.delete(like)
            db.session.commit()

            return content, 212

        return content, 210
