from django.shortcuts import render, get_object_or_404
from django.urls import reverse,reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.views.generic import (CreateView, TemplateView, UpdateView,
                                  DeleteView, ListView, DetailView,
                                  RedirectView)
from .models import Community, CommunityMember
from django.utils import timezone

# Create your views here.

class CreateCommunity(LoginRequiredMixin, CreateView):
    """ Just users who logged in can create Community 
    returns 'community' as lower case as context
    """
    model = Community
    template_name_suffix = '_create_form'
    fields = ('name', 'description')

class CommunityDetail(DetailView): #SingleCommunity
    """ show Community Detail 
        returns 'community' as lower case as context
    """
    model = Community
    # context can be 'community' ot 'object'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        community = self.get_object()
        members = community.members.all()  # Retrieve all members of the community
        context['members'] = members
        return context
    
class about_comm(TemplateView):
    template_name = "communities/about_com.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = Community.objects.all()[:5]
        return context

class ListCommunity(ListView):
    """ List All Communities - returns 'community_list' as lower case as context"""
    model = Community
 
class CommunityMembersListView(ListView):
    model = Community
    template_name = 'communities/community_members_list.html'  # Create this template
    context_object_name = 'communities'  # The context variable to access communities
    
    def get_queryset(self):
        return Community.objects.all()
    
class JoinCommunity(LoginRequiredMixin, RedirectView):
    # redirect after join
    def get_redirect_url(self, *args, **kwargs):
        return reverse('communities:single', kwargs={'slug':self.kwargs.get('slug')})
    
    # check if user is in community
    def get(self, request, *args, **kwargs):
        community_in = get_object_or_404(Community, slug=self.kwargs.get('slug'))
        
        try:
            CommunityMember.objects.create(user=self.request.user, community= community_in)

        except IntegrityError:
            messages.warning(self.request,("Warning, already a member of {}".format(community_in.name)))

        else:
            messages.success(self.request,"You are now a member of the {} group.".format(community_in.name))

        return super().get(request, *args, **kwargs)
    
class UpdateCommunity(UpdateView):
    model = Community
    fields = ('description',)
    template_name_suffix = '_update_form'

class LeaveCommunity(LoginRequiredMixin, RedirectView):
    # redirect after leave
    def get_redirect_url(self, *args, **kwargs):
        return reverse('communities:single', kwargs={'slug': self.kwargs.get("slug")})
    
    # check if user is in community
    def get(self, request, *args, **kwargs):
        try:
            memberships = CommunityMember.objects.filter(
                user=self.request.user,
                community__slug=self.kwargs.get("slug")
            ).get()
        except CommunityMember.DoesNotExist:
            messages.warning(
                self.request,
                "You can't leave this group because you aren't in it."
            )
        else:
            memberships.delete()
            messages.success(
                self.request,
                "You have successfully left this group."
            )
        return super().get(request, *args, **kwargs)