from django.contrib import admin
from post_app.models import Post,Comment, PostLike
# Register your models here.

class CommentAdmin(admin.ModelAdmin):
    list_display=('id', 'text', 'is_reply')

class PostLikeAdmin(admin.ModelAdmin):
    list_display=('id', 'user', 'post', 'is_like')

class PostAdmin(admin.ModelAdmin):
    list_display=('id', 'user', 'content')

admin.site.register(Comment, CommentAdmin)
admin.site.register(PostLike, PostLikeAdmin)
admin.site.register(Post, PostAdmin)