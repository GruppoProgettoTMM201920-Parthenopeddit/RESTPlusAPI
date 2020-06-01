from flask_restplus import Namespace, Resource

# TODO add description
api = Namespace('Messages', description='')


@api.route("/")
class Message(Resource):
    def get(self):
        return {}, 200