from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Profile(models.Model):
    GENDER_CHOICES = [
        ('M', _('Male')),
        ('F', _('Female')),
        ('O', _('Other')),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True, verbose_name=_('Gender'))
    bio = models.TextField(blank=True, null=True, verbose_name=_('Bio'))
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True, verbose_name=_('Profile Image'))
    dob = models.DateField(blank=True, null=True, verbose_name=_('Date of Birth'))

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')
        ordering = ['user__username']

    def __str__(self):
        return f"{self.user.username}'s Profile"

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(verbose_name=_('Content'))
    reposted_from = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='reposts', verbose_name=_('Reposted From'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    likes = models.IntegerField(default=0, verbose_name=_('Likes Count'))
    comment_count = models.IntegerField(default=0, verbose_name=_('Comments Count'))  # Renamed from 'comments'
    shares = models.IntegerField(default=0, verbose_name=_('Shares Count'))

    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['author']),
        ]

    def __str__(self):
        return f"Post by {self.author.username} at {self.created_at}"

    def is_repost(self):
        return self.reposted_from is not None

class PostMedia(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='media')
    image = models.ImageField(upload_to='post_media/', verbose_name=_('Image'))

    class Meta:
        verbose_name = _('Post Media')
        verbose_name_plural = _('Post Media')
        ordering = ['id']

    def __str__(self):
        return f"Media for Post {self.post.id}"

class PostLiked(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='liked_by')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_posts')

    class Meta:
        verbose_name = _('Post Like')
        verbose_name_plural = _('Post Likes')
        unique_together = ('post', 'user')

    def __str__(self):
        return f"{self.user.username} liked Post {self.post.id}"

    def save(self, *args, **kwargs):
        created = not self.pk  # Check if this is a new instance
        super().save(*args, **kwargs)
        if created:
            self.post.likes += 1
            self.post.save(update_fields=['likes'])

    def delete(self, *args, **kwargs):
        if self.post.likes > 0:
            self.post.likes -= 1
            self.post.save(update_fields=['likes'])
        super().delete(*args, **kwargs)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments_authored')
    content = models.TextField(verbose_name=_('Content'))
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies', verbose_name=_('Parent Comment'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))
    likes = models.IntegerField(default=0, verbose_name=_('Likes Count'))

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['post', 'created_at']),
            models.Index(fields=['parent']),
        ]

    def __str__(self):
        return f"Comment by {self.author.username} on Post {self.post.id}"

    def is_reply(self):
        return self.parent is not None

    def save(self, *args, **kwargs):
        created = not self.pk
        super().save(*args, **kwargs)
        if created:
            self.post.comment_count += 1
            self.post.save(update_fields=['comment_count'])

    def delete(self, *args, **kwargs):
        if self.post.comment_count > 0:
            self.post.comment_count -= 1
            self.post.save(update_fields=['comment_count'])
        super().delete(*args, **kwargs)

class CommentLiked(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='liked_by')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_comments')

    class Meta:
        verbose_name = _('Comment Like')
        verbose_name_plural = _('Comment Likes')
        unique_together = ('comment', 'user')

    def __str__(self):
        return f"{self.user.username} liked Comment {self.comment.id}"

    def save(self, *args, **kwargs):
        created = not self.pk
        super().save(*args, **kwargs)
        if created:
            self.comment.likes += 1
            self.comment.save(update_fields=['likes'])

    def delete(self, *args, **kwargs):
        if self.comment.likes > 0:
            self.comment.likes -= 1
            self.comment.save(update_fields=['likes'])
        super().delete(*args, **kwargs)


