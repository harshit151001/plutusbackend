from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, LikeViewSet, login, signup

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'likes', LikeViewSet)


urlpatterns = [
    path('', include(router.urls)),
    re_path('signup', signup),
    re_path('login', login)
]