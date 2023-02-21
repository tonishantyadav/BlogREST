from django.urls import path
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('posts', views.PostViewSet, basename='post')
router.register('authors', views.AuthorViewSet, basename='author')

post_router = routers.NestedDefaultRouter(router, 'posts', lookup='post')
post_router.register('reviews', views.ReviewViewSet, basename='post-reviews')

urlpatterns = router.urls + post_router.urls
