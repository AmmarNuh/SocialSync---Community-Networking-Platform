from django.urls import path
from . import views
from .models import Post

from django.views.generic.dates import ArchiveIndexView


app_name = 'posts'


urlpatterns = [
    path('', views.UserPosts.as_view(), name= 'all_posts'), #all
    path('list', views.PostListView.as_view(), name= 'post_list'), #all
    path('new', views.CreatePost.as_view(), name= 'new_post'), #crete
    path('by/<username>/', views.UserPosts.as_view(), name= 'for_user'),
    path('by/<username>/<int:pk>', views.PostDetailView.as_view(), name= 'post_detali'),  #single
    path('delete/<int:pk>', views.DeletePost.as_view(), name= 'delete_post'),
    path('edit/<int:pk>', views.PostUpdateView.as_view(), name= 'edit_post'),

    
    
    path(
        "archive/",
        ArchiveIndexView.as_view(model=Post, date_field="created_at"),
        name="post_archive"),
]
