from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class ProgressPost(models.Model):
    """
    User progress updates with images
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress_posts')
    title = models.CharField(max_length=100)
    caption = models.TextField(max_length=500, blank=True)
    image = models.ImageField(upload_to='porgress_posts/', blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.title[:30]}"

    def get_absolute_url(self):
        return reverse('community:post_detail', kwargs={"pk": self.pk})
    
    def total_likes(self):
        return self.likes.count()
    
    def get_comments_count(self):
        return self.comments.count()
    

class Comment(models.Model):
    """
    Comments on progress posts
    """

    post = models.ForeignKey(ProgressPost, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.content[:30]}"
    

