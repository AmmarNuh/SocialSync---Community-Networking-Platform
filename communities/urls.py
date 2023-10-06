from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from posts.models import Post

from django.views.generic.dates import ArchiveIndexView



app_name = 'communities'

urlpatterns = [
    path('', views.ListCommunity.as_view(), name= 'list_comm'), #all
    path('new', views.CreateCommunity.as_view(), name= 'new_comm'), #crete
    path(r'^posts/in/(?P<slug>[-a-zA-Z0-9_؀-ۿ]+)/$', views.CommunityDetail.as_view(), name= 'single'), 
    path(r'^join/(?P<slug>[-a-zA-Z0-9_؀-ۿ]+)/$', views.JoinCommunity.as_view(), name= 'join'), 
    path(r'^leave/(?P<slug>[-a-zA-Z0-9_؀-ۿ]+)/$', views.LeaveCommunity.as_view(), name= 'leave'), 
    path(r'^update/(?P<slug>[-a-zA-Z0-9_؀-ۿ]+)/$', views.UpdateCommunity.as_view(), name= 'update'),
    path('members/', views.CommunityMembersListView.as_view(), name='community_members_list'),


    path('about', views.about_comm.as_view(extra_context={"title": "this is an extra context"}), name= 'about'),
    path(
        "archive/",
        ArchiveIndexView.as_view(model=Post, date_field="created_at"),
        name="post_archive"),
    
]

