
from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    user=models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='media/images/posts/', null=True, blank=True)
    is_private = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)  
    def __str__(self):
        return str(self.id)
    

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_reply=models.BooleanField(default=False)
    def __str__(self):
        return str(self.id)
    
class PostLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_like=models.BooleanField()
    
    def __str__(self):
        return str(self.id)
    # class Meta:
    #     unique_together = ['user', 'post']
    
# class Follower(models.Model):
#     follower = models.ForeignKey(CustomUser, related_name='following', on_delete=models.CASCADE)
#     following = models.ForeignKey(CustomUser, related_name='followers', on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)



# class Chat(models.Model):
#     created_at = models.DateTimeField(auto_now_add=True)
# class Participant(models.Model):
#     chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     joined_at = models.DateTimeField(auto_now_add=True)
# class Message(models.Model):
#     chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     content = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
