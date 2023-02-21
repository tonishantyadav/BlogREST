from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Post, Author, Review

User = get_user_model()

class PostSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user_id = self.context.get('user_id')
        try:
            user = User.objects.get(pk=user_id)
            (author, created) = Author.objects.get_or_create(user_id=user_id)
            post = Post.objects.create(**validated_data, author_id=author.id)
            post.save()
            return post
        except User.DoesNotExist:
            raise serializers.ValidationError('You need to register first to create any post.')

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'date_posted', 'last_updated', 'author_id']
        read_only_fields = ['author_id']


class AuthorSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()

    def validated_user_id(self, value):
        if not User.objects.filter(pk=value).exists():
            raise serializers.ValidationError('No registration detail found of the user.')
        return value

    def save(self, **kwargs):
        try:
            author = Author.objects.get(user_id=self.validated_data.get('user_id'))
            raise serializers.ValidationError('No duplicate entry allowed.')
        except Author.DoesNotExist:
            author = Author.objects.create(**self.validated_data)
            self.instance = author
        return self.instance

    class Meta:
        model = Author
        fields = ['id', 'user_id', 'birth_date', 'phone']


class SimpleAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'birth_date', 'phone']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'name', 'description', 'date']
