from rest_framework import serializers
from post_app.models import Post, Comment, PostLike

class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model=Comment
        fields=('id', 'text', 'created_at', 'post') 
        read_only_fields = ('post',)
        
class CommentSerializer(serializers.ModelSerializer):
    replies=ReplySerializer(many=True, read_only=True)
    reply_count=serializers.SerializerMethodField()
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model=Comment
        fields =('id', 'user', 'text', 'reply_count', 'replies' )
    def get_reply_count(self,instance):
        count=Comment.objects.filter(parent_comment=instance).count()
        return count
        
class PostSerializer(serializers.ModelSerializer):
    # comments=CommentSerializer(many=True, read_only=True)
    user = serializers.ReadOnlyField(source='user.username')
    comments=serializers.SerializerMethodField()
    total_comments=serializers.SerializerMethodField()
    total_likes=serializers.SerializerMethodField()
    total_dislikes=serializers.SerializerMethodField()
    liked_by = serializers.SerializerMethodField()
    disliked_by = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields =('id', 'user', 'content', 'image', 'total_likes','total_dislikes', 'liked_by', 'disliked_by', 'total_comments', 'comments')
    
    def get_total_comments(self,instance):
        comment_count=Comment.objects.filter(post_id=instance.id).count()
        return comment_count
    
    def get_comments(self,instance):
        comments=CommentSerializer(instance.comments.filter(is_reply=False),many=True)
        return comments.data
    
    def get_total_likes(self,instance):
        likes_count=PostLike.objects.filter(post_id=instance.id, is_like=True).count()
        return likes_count
    
    def get_total_dislikes(self,instance):
        dislike_count=PostLike.objects.filter(post_id=instance.id, is_like=False).count()
        return dislike_count
    
    def get_liked_by(self, instance):
        liked_users = PostLike.objects.filter(post_id=instance.id, is_like=True).values_list('user__username',flat=True)
        return liked_users
    
    def get_disliked_by(self, instance):
        disliked_users = PostLike.objects.filter(post_id=instance.id, is_like=False).values_list('user__username',flat=True)
        return disliked_users
    
class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model=PostLike
        fields='__all__'
        read_only_fields = ('post', 'user', 'created_at')
    
    
