from django.urls import path
from .views import PostListView, CommentView, CommentDetailView, PostDetailView, ReplyView, PostLikeCreateView

urlpatterns = [
    path('api/posts/', PostListView.as_view(), name='posts'),
    path('api/posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('api/posts/<int:pk>/comments/', CommentView.as_view(), name='comments'),
    path('api/posts/<int:post_id>/comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
    path('api/posts/<int:post_id>/comment/<int:parent_comment_id>/reply/', ReplyView.as_view(), name='reply'),
    path('api/posts/<int:post_id>/like/', PostLikeCreateView.as_view(), name='post-like'),
    
    # path('api/comments/', CommentListView.as_view(), name='comment-list'),
    # path('api/comment/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
]
