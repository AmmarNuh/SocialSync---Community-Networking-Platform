from django.db import models
from django.urls import reverse
from django.conf import settings
import misaka
from django.contrib import admin
from django.utils import timezone
import datetime

from django.contrib.auth import get_user_model
User = get_user_model()

from communities.models import Community


# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(User, related_name='posts', verbose_name="Post Writer", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    message = models.TextField()
    message_html = models.TextField(editable=False)
    community = models.ForeignKey(Community, related_name='posts', 
                                  null=True, blank=True, 
                                  verbose_name="post in community", on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ['-created_at']         # ordered DSAC
        unique_together = ('user', 'message')         # every message is uniquely linked to user

    def save(self, *args, **kwargs):
        self.message_html = misaka.html(self.message)
        super().save(*args, **kwargs)
        
    def get_absolute_url(self):
        return reverse("posts:post_detali", 
                       kwargs={"username":self.user.username,
                               "pk":self.pk})

    def __str__(self):
        return self.message
    

    @admin.display(
        boolean=True,
        ordering="created_at",
        description="Published recently?",
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.created_at <= now