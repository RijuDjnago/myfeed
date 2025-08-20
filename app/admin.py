from django.contrib import admin
from .models import Profile, Post, PostMedia, PostLiked, Comment, CommentLiked

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'dob', 'bio_preview')
    search_fields = ('user__username', 'user__email', 'bio')
    list_filter = ('gender',)
    readonly_fields = ('user',)

    def bio_preview(self, obj):
        return obj.bio[:50] + '...' if obj.bio and len(obj.bio) > 50 else obj.bio
    bio_preview.short_description = 'Bio Preview'

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'content_preview', 'created_at', 'likes', 'comment_count', 'shares', 'is_repost', 'reposted_from')
    search_fields = ('author__username', 'content')
    list_filter = ('created_at',)
    readonly_fields = ('created_at', 'likes', 'comment_count', 'shares')
    raw_id_fields = ('reposted_from',)
    autocomplete_fields = ('author',)

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content Preview'

@admin.register(PostMedia)
class PostMediaAdmin(admin.ModelAdmin):
    list_display = ('post', 'image')
    search_fields = ('post__id',)
    raw_id_fields = ('post',)

@admin.register(PostLiked)
class PostLikedAdmin(admin.ModelAdmin):
    list_display = ('user', 'post')
    search_fields = ('user__username', 'post__id')
    raw_id_fields = ('post', 'user')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'content_preview', 'created_at', 'likes', 'is_reply', 'parent')
    search_fields = ('author__username', 'content', 'post__id')
    list_filter = ('created_at',)
    readonly_fields = ('created_at', 'updated_at', 'likes')
    raw_id_fields = ('post', 'parent', 'author')

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content Preview'

@admin.register(CommentLiked)
class CommentLikedAdmin(admin.ModelAdmin):
    list_display = ('user', 'comment')
    search_fields = ('user__username', 'comment__id')
    raw_id_fields = ('comment', 'user')