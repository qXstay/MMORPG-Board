from django.urls import path, include
from .views import (
    PostListView, PostDetailView, PostCreateView,
    ResponseCreateView, ResponseListView, PostUpdateView, PostDeleteView
)

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/create/', PostCreateView.as_view(), name='post_create'),
    path('post/edit/<int:pk>/', PostUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('post/<int:pk>/response/', ResponseCreateView.as_view(), name='create_response'),
    path('responses/', ResponseListView.as_view(), name='response_list'),
]