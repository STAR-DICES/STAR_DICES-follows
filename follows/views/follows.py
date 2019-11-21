from flakon import SwaggerBlueprint
from flask import request, jsonify, abort
from sqlalchemy.exc import IntegrityError
from follows.database import db, Follow
from werkzeug.security import generate_password_hash, check_password_hash
from jsonschema import validate, ValidationError
from datetime import datetime

follows = SwaggerBlueprint('follows', 'follows', swagger_spec='./follows/static/follows-specs.yaml')


def general_validator(op_id, request):
    schema= follows.spec['paths']
    for endpoint in schema.keys():
        for method in schema[endpoint].keys():
            if schema[endpoint][method]['operationId']==op_id:
                op_schema= schema[endpoint][method]['parameters'][0]
                if 'schema' in op_schema:
                    definition= op_schema['schema']['$ref'].split("/")[2]
                    schema= follows.spec['definitions'][definition]
                    try:
                        validate(request.get_json(), schema=schema)
                        return True
                    except ValidationError as error:
                        return False
                else:
                     return True

"""
This route lets a logged user follow another user.

@users.route('/wall/<int:author_id>/follow', methods=['GET'])
@login_required
def follow(author_id):
    message = ''
    if author_id==current_user.id:
        message= "Cannot follow yourself"
    else:
        author = User.query.filter_by(id = author_id).first()
        if author is None:
            abort(404)
            
        db.session.add(Follow(author_id, current_user.id))
        try:
            db.session.commit()
            message = "Following!"
        except IntegrityError:
            db.session.rollback()
            message = "Already following!"
    return render_template('message.html', message = message)
"""
"""
This route lets a logged user unfollow a followed user.

@users.route('/wall/<int:author_id>/unfollow', methods=['GET'])
@login_required
def unfollow(author_id):
    message = ''
    if author_id==current_user.id:
        message= "Cannot unfollow yourself"
    else:
        author = User.query.filter_by(id = author_id).first()
        if author is None:
            abort(404)
        if isFollowing(author_id, current_user.id) :
            Follow.query.filter(Follow.user_id == author_id, Follow.followed_by_id == current_user.id).delete()
            db.session.commit()
            message = "Unfollowed!"
        else:
            message = "You were not following that particular user!"
    return render_template('message.html', message = message)
"""
"""
This route lets a logged user see his own followers.
"""

@follows.operation('followers-list')
def my_followers(writer_id):
    followers = (db.session.query(Follow).filter(Follow.user_id == writer_id)
                                           .filter(Follow.followed_by_id != writer_id)
                                           .all())

    return jsonify({'followers': [{'follower_id': obj.followed_by_id, 'follower_name': obj.followed_by_name} for obj in followers]})
