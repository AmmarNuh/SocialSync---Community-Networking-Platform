from django.shortcuts import render
from django.urls import reverse,reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (CreateView, TemplateView, UpdateView,
                                  DeleteView, ListView, DetailView)
from django.http import Http404

from .models import Post
from . import forms

from braces.views import SelectRelatedMixin

from django.contrib.auth import get_user_model
User = get_user_model()
# Create your views here.


class PostListView(SelectRelatedMixin, ListView):
    model = Post
    # to which user the post related to, and in which comm
    select_related = ('user', 'community')
    

class UserPosts(ListView):
    model = Post
    template_name = "posts/user_post_list.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_user"] = self.post_user
        return context

    def get_queryset(self):
        try:
            # checks if username == current logged in username
            self.post_user = User.objects.prefetch_related("posts").get(username__iexact=self.kwargs.get("username"))        
        except User.DoseNotExist:
            raise Http404
        finally:
            return self.post_user.posts.all()
        

class PostListView(ListView):
    model = Post
    template_name = "posts/post_list.html"
    
    # def get_context_data(self, **kwargs):
    #     members = Post.message # Retrieve all members of the community
    #     context['posts'] = members
    #     return context


class PostDetailView(SelectRelatedMixin, DetailView):
    model = Post
    select_related = ('user', 'community',)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__username__iexact=self.kwargs.get('username'))


class CreatePost(LoginRequiredMixin, SelectRelatedMixin, CreateView):
    model = Post
    fields = ('message', 'community')
    select_related = ('user', 'community')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class DeletePost(LoginRequiredMixin, SelectRelatedMixin, DeleteView):
    model = Post
    select_related = ('user', 'community')
    success_url = reverse_lazy('posts:all_posts')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request, 'Post Deleted.!')
        return super().delete(user_id=self.request.user.id)


class PostUpdateView(UpdateView):
    model = Post
    # template_name = "TEMPLATE_NAME"
    template_name_suffix = '_update_form'

    fields = ('message', 'community',) 
