from django.contrib import admin
from .models import Post

# Register your models here.
from communities.models import Community



    
class ChoiceInline(admin.StackedInline):
    model = Post
    extra = 1


class PostAdmin(admin.ModelAdmin):
    list_display = ["message", "user", "community", "created_at", "was_published_recently"]
    list_filter = ["message"]
    list_editable = ["user",'community']
    search_fields = ["message"]
    
    

admin.site.register(Post, PostAdmin)