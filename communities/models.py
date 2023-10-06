from django.db import models
from django.utils.text import slugify
from django.urls import reverse,reverse_lazy

import misaka
from django.contrib.auth import get_user_model
User = get_user_model()

from django import template
register = template.Library()

# Create your models here.
########## Community Model #############

class Community(models.Model):
    """ each Community has a unique name, unique slug, description, and members """
    name = models.CharField( unique=True , max_length=80, verbose_name="Community Nmae")
    slug = models.SlugField( allow_unicode=True, unique=True )
    description = models.TextField(blank=True, default='', verbose_name="Community Description")
    description_html = models.TextField(blank=True, default='', editable=False)
    # Many 'users' for 'Community', and 'user' can be in Many 'Community' 
    members = models.ManyToManyField(User, through='CommunityMember', verbose_name="Community Members")

    class Meta:
        verbose_name = "Community"
        verbose_name_plural = "Communities"
        ordering = ['name']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        self.description_html = misaka.html(self.description)
        super().save(*args, **kwargs)
        
    def get_absolute_url(self):
        return reverse("communities:single", kwargs={"slug": self.slug})

    def __str__(self):
        return self.name



########## CommunityMember Model #############
class CommunityMember(models.Model):
    community = models.ForeignKey(Community, related_name='memberships', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user_communities', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Community Member"
        verbose_name_plural = "Community Members"
        
        unique_together = ('community', 'user')

    def __str__(self):
        return self.user.username
