from django.urls import path
from .views import (
    RegisterView, LoginView, LogoutView,
    UserProfileListAPIView, UserProfileDetailAPIView,
    PostListAPIView, PostDetailAPIView, PostCreateAPIView,
    CommentsListAPIView, CommentsDetailAPIView, CommentsCreateAPIView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/', UserProfileListAPIView.as_view(), name='user_list'),
    path('user/<int:pk>/', UserProfileDetailAPIView.as_view(), name='user_detail'),
    path('post/', PostListAPIView.as_view(), name='post_list'),
    path('post/create/', PostCreateAPIView.as_view(), name='post_create'),
    path('post/<int:pk>/', PostDetailAPIView.as_view(), name='post_detail'),
    path('post/<int:post_pk>/comments/', CommentsListAPIView.as_view(), name='comments_list'),
    path('post/<int:post_pk>/comments/create/', CommentsCreateAPIView.as_view(), name='comments_create'),
    path('comments/<int:pk>/', CommentsDetailAPIView.as_view(), name='comments_detail'),
]
