from flakon import SwaggerBlueprint
from flask import request, jsonify, abort
from sqlalchemy.exc import IntegrityError
from follows.database import db, Follow
from werkzeug.security import generate_password_hash, check_password_hash
from jsonschema import validate, ValidationError
from datetime import datetime

follows = SwaggerBlueprint('follows', 'follows', swagger_spec='./follows-specs.yaml')

"""
This endpoint returns the followers list with their id and name
"""
@follows.operation('followers-list')
def my_followers(user_id):
    followers = (db.session.query(Follow).filter(Follow.user_id == user_id)
                                           .filter(Follow.followed_by_id != user_id)
                                           .all())

    return jsonify({'followers': [{'follower_id': obj.followed_by_id, 'follower_name': obj.followed_by_name} for obj in followers]})

"""
This endpoint returns the following list ids
"""
@follows.operation('following-list')
def my_following(user_id):
    following = (db.session.query(Follow).filter(Follow.followed_by_id == user_id)
                                           .all())

    return jsonify({'following_ids': [obj.user_id for obj in following]})

"""
This endpoint creates an entry in the db allowing a user to follow another user
"""
@follows.operation('follow')
def follow():
    if general_validator('follow', request):
        json_data= request.get_json()
        user_id= json_data['user_id']
        user_name= json_data['user_name']
        followee_id= json_data['followee_id']
        db.session.add(Follow(followee_id, user_id, user_name))
        db.session.commit()
        return "Following", 200
    else:
        return abort(400)

"""
This endpoint deletes a follow entry
"""
@follows.operation('unfollow')
def unfollow():
    if general_validator('unfollow', request):
        json_data= request.get_json()
        user_id= json_data['user_id']
        followee_id= json_data['followee_id']
        Follow.query.filter(Follow.user_id == followee_id, Follow.followed_by_id == user_id).delete()
        return "Unfollowed", 200
    else:
        return abort(400)

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