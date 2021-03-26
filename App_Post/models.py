from django.db import models
from django.conf import settings

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_post')
    image = models.ImageField(upload_to='post_images')
    caption = models.CharField(max_length=264)
    upload_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.caption[:20]

    class Meta:
        ordering = ['-upload_date', ]

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='liked_post')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='liker')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} : {}'.format(self.user.username, self.post.caption)
