from django.contrib import admin
from .models import Community, CommunityMember
from posts.models import Post


class CommunityMemberInline(admin.TabularInline):
    '''Tabular Inline View for '''

    model = CommunityMember
    # min_num = 3
    # max_num = 20
    # extra = 1
    # raw_id_fields = (,)
    
    
class ChoiceInline(admin.StackedInline):
    model = Post
    extra = 0


class CommunityAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Community:', {"fields": ["name",  ]}),
        ("Community information", {"fields": ["slug","description"], "classes": ["collapse"]}),
    ]
    inlines = [ChoiceInline]
    list_display = ["name", "description"]
    list_filter = ["name"]
    search_fields = ["name"]
    # list_editable = ["name"]


admin.site.register(Community, CommunityAdmin)




