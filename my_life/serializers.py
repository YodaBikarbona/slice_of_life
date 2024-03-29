from rest_framework import serializers
from .models import (
    User,
    Role,
    Image,
    Post,
    ImageComment,
    PostComment,
    Album
)


class RoleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Role
        fields = [
            'id',
            'name'
        ]


class UserSerializer(serializers.HyperlinkedModelSerializer):
    role = RoleSerializer(many=False)

    class Meta:
        model = User
        fields = [
            'id',
            'user_name',
            'email',
            'activated',
            'newsletter',
            'role',
        ]


class AlbumSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Album
        fields = [
            'id',
            'created',
            'name',
        ]


class ImageSerializer(serializers.HyperlinkedModelSerializer):
    album = AlbumSerializer(many=False)

    class Meta:
        model = Image
        fields = [
            'id',
            'created',
            'google_drive_link',
            'description',
            'comment',
            'views',
            'likes',
            'type',
            'path',
            'uniqueId',
            'album'
        ]


class ImageCommentSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(many=False)
    image = ImageSerializer(many=False)

    class Meta:
        model = ImageComment
        fields = [
            'id',
            'created',
            'content',
            'approved',
            'user',
            'image',
        ]


class PostSerializer(serializers.HyperlinkedModelSerializer):
    image = ImageSerializer(many=False)

    class Meta:
        model = Post
        fields = [
            'id',
            'created',
            'edited',
            'title',
            'content',
            'comment',
            'views',
            'image',
            'uniqueId'
        ]


class PostCommentSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(many=False)
    post = PostSerializer(many=False)

    class Meta:
        model = ImageComment
        fields = [
            'id',
            'created',
            'content',
            'approved',
            'user',
            'post',
        ]
