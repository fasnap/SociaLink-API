from django.shortcuts import get_object_or_404
from rest_framework import generics
from . permissions import IsOwnerOrReadOnly,IsAuthenticatedOrReadOnly
from post_app.models import Post,Comment,PostLike
from .serializers import PostSerializer,CommentSerializer,ReplySerializer, PostLikeSerializer
from rest_framework.permissions import IsAuthenticated

class PostListView(generics.ListCreateAPIView):
    queryset=Post.objects.all()
    serializer_class= PostSerializer
    permission_classes=[IsAuthenticatedOrReadOnly ]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Post.objects.all()
    serializer_class=PostSerializer
    permission_classes=[IsOwnerOrReadOnly,]
    
class CommentView(generics.ListCreateAPIView):
    serializer_class= CommentSerializer
    permission_classes=[IsAuthenticatedOrReadOnly ]
    
    def get_queryset(self):
        post_id=self.kwargs['pk']
        return Comment.objects.filter(post_id=post_id, is_reply=False)
    
    def perform_create(self, serializer):
        post_id=self.kwargs['pk']
        serializer.save(post_id=post_id, user=self.request.user)

class ReplyView(generics.ListCreateAPIView):
    serializer_class=ReplySerializer
    permission_classes=[IsAuthenticatedOrReadOnly ]
    
    def get_queryset(self):
        post_id=self.kwargs['post_id']
        parent_comment_id=self.kwargs['parent_comment_id']
        return Comment.objects.filter(post_id=post_id, parent_comment_id=parent_comment_id, is_reply=True)

    def perform_create(self,serializer):
        post_id=self.kwargs['post_id']
        parent_comment_id=self.kwargs['parent_comment_id']
        post=get_object_or_404(Post, id = post_id)
        parent_comment=get_object_or_404(Comment, id = parent_comment_id, post=post)
        serializer.save(post=post, parent_comment=parent_comment, is_reply=True)
        
class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class= CommentSerializer
    permission_classes=[IsOwnerOrReadOnly ]
    
    def get_queryset(self):
        post_id=self.kwargs['post_id']
        return Comment.objects.filter(post_id=post_id, is_reply=False)

class PostLikeCreateView(generics.CreateAPIView):
    serializer_class=PostLikeSerializer
    permission_classes=[IsAuthenticated]
    
    def perform_create(self, serializer):
        user=self.request.user
        post_id=self.kwargs['post_id']
        try:
            like_data=PostLike.objects.get(user=user, post_id=post_id)
            like_data.is_like = not like_data.is_like
            like_data.save()
        except PostLike.DoesNotExist:
            serializer.save(user=user, post_id=post_id)
       
# class CommentListView(generics.ListAPIView):
#     queryset=Comment.objects.filter(is_reply=False)
#     serializer_class=CommentSerializer