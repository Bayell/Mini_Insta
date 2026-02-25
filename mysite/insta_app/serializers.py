from rest_framework import serializers
from .models import (
    UserProfile, Follow, Hashtag, Post, PostContent,
    PostLike, Comments, CommentLike, Favorite, FavoriteItem
)
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password', 'avatar', 'bio', 'phone_number', 'birth_date', 'date_registered')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError('неправильные данные')

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class UserProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'avatar', 'username', 'is_official']


class UserProfileDetailSerializer(serializers.ModelSerializer):
    date_registered = serializers.DateField(format='%d-%m-%Y')

    class Meta:
        model = UserProfile
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'avatar',
                  'bio', 'user_link', 'is_official', 'phone_number', 'birth_date', 'date_registered']


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ['id', 'hashtag_name']


class PostContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostContent
        fields = ['id', 'file']


class PostListSerializer(serializers.ModelSerializer):
    author = UserProfileListSerializer()
    hashtag = HashtagSerializer(many=True)
    created_date = serializers.DateField(format='%d-%m-%Y')

    class Meta:
        model = Post
        fields = ['id', 'author', 'description', 'hashtag', 'created_date']


class PostDetailSerializer(serializers.ModelSerializer):
    author = UserProfileListSerializer()
    hashtag = HashtagSerializer(many=True)
    contents = PostContentSerializer(many=True, read_only=True)
    created_date = serializers.DateField(format='%d-%m-%Y')

    class Meta:
        model = Post
        fields = ['id', 'author', 'description', 'music', 'hashtag', 'user', 'contents', 'created_date']


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['description', 'music', 'hashtag', 'user']


class CommentsSerializer(serializers.ModelSerializer):
    user = UserProfileListSerializer()
    created_date = serializers.DateField(format='%d-%m-%Y')

    class Meta:
        model = Comments
        fields = ['id', 'user', 'text', 'parent', 'created_date']


class CommentsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ['text', 'parent']
