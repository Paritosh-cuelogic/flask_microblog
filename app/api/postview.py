from flask import jsonify
from flask_restful import Resource, Api, request

from app.api import api
from flask_jwt import jwt_required, current_identity
from app.post.models import Post
from app import db
from app.auth.models import BlogUser


class Posts(Resource):
    def get(self):
        posts = Post.query.order_by(Post.timestamp.desc()).all()
        post_list = []
        for post in posts:
            post_list.append({
                'avatar': post.author.avatar(70),
                'username': post.author.username,
                'body': post.body
            })
        return {'data': post_list}

    @jwt_required()
    def post(self):
        data = request.get_json()
        print(current_identity)
        post = Post(body=data['body'], author=current_identity)
        db.session.add(post)
        db.session.commit()
        return {'status': True, 'id': post.id}


class FollowingPosts(Resource):
    @jwt_required()
    def get(self):
        posts = current_identity.followed_posts().all()
        post_list = []
        for post in posts:
            post_list.append({
                'avatar': post.author.avatar(70),
                'username': post.author.username,
                'body': post.body
            })
        return {'data': post_list}


class Profile(Resource):
    @jwt_required()
    def get(self):
        return {'username': current_identity.username, 'about_me':current_identity.about_me}

    @jwt_required()
    def put(self):
        data = request.get_json()
        current_identity.username = data['username']
        current_identity.about_me = data['about_me']
        db.session.commit()
        return {'username': current_identity.username, 'about':current_identity.about_me}


class Follow(Resource):
    @jwt_required()
    def get(self, id):
        try:
            user = BlogUser.query.filter_by(id=id).first()
            current_identity.follow(user)
            db.session.commit()
            return {'result': True}
        except:
            return {'result': False}


class Unfollow(Resource):
    @jwt_required()
    def get(self, id):
        try:
            user = BlogUser.query.filter_by(id=id).first()
            current_identity.unfollow(user)
            db.session.commit()
            return {'result': True}
        except:
            return {'result': False}


api.add_resource(Posts, '/posts')
api.add_resource(FollowingPosts, '/post')
api.add_resource(Profile, '/profile')
api.add_resource(Follow, '/follow/<int:id>')
api.add_resource(Unfollow, '/unfollow/<int:id>')
