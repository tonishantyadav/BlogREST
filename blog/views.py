from django.shortcuts import redirect
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from .permissions import IsAdminOrAuthor
from .models import Post, Author, Review
from .serializers import (PostSerializer, AuthorSerializer,
    SimpleAuthorSerializer, ReviewSerializer)


class PostViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'delete']

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['author_id', 'title']

    def get_permissions(self):
        if self.request.method in ['GET']:
            return [AllowAny()]
        elif self.request.method in ['POST']:
            return [IsAuthenticated()]
        return [IsAdminOrAuthor()] 

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return redirect('post-list')
    
    def retrieve(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('post-list')
        return super().retrieve(request, *args, **kwargs)

    
class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.action == 'me':
            return SimpleAuthorSerializer
        return AuthorSerializer

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        (author, created) = Author.objects.get_or_create(user_id=request.user.id)
        if request.method == 'GET':
            serializer = SimpleAuthorSerializer(author)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = SimpleAuthorSerializer(author, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Review.objects.filter(post_id=self.kwargs.get('post_pk'))
