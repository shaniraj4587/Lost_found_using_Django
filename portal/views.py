from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q

from .models import Item, ItemImage, Comment
from .forms import ItemReportForm, CommentForm

class HomeView(TemplateView):
    """
    Displays the home page with the 5 most recent lost and found items.
    """
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_lost_items'] = Item.objects.filter(
            item_type='lost', 
            is_approved=True
        ).order_by('-reported_at')[:5]
        
        context['recent_found_items'] = Item.objects.filter(
            item_type='found', 
            is_approved=True
        ).order_by('-reported_at')[:5]
        return context

class ItemListView(ListView):
    """
    Displays a full list of all approved items, filterable by type and search.
    """
    model = Item
    template_name = "portal/item_list.html"
    context_object_name = "items"
    paginate_by = 12

    def get_queryset(self):
        # Start with all approved items
        queryset = super().get_queryset().filter(is_approved=True).order_by('-reported_at')
        
        # Filter by item type (lost/found)
        item_type = self.request.GET.get('type')
        if item_type in ['lost', 'found']:
            queryset = queryset.filter(item_type=item_type)
            
        # Filter by search query
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(location__icontains=query)
            )
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass filter params back to template for display
        context['item_type'] = self.request.GET.get('type', '')
        context['query'] = self.request.GET.get('q', '')
        return context


class ItemDetailView(DetailView):
    """
    Displays the full details of a single item, including images and comments.
    """
    model = Item
    template_name = "portal/item_detail.html"
    context_object_name = "item"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add comment form and list of comments
        context['comment_form'] = CommentForm()
        context['comments'] = self.object.comments.all()
        # Add all images for the carousel
        context['item_images'] = self.object.images.all()
        return context
    
    def get_queryset(self):
        # Only allow viewing of approved items
        return super().get_queryset().filter(is_approved=True)

class CommentCreateView(LoginRequiredMixin, CreateView):
    """
    View to handle POST requests for creating a new comment.
    This view is not rendered directly; it just processes the form.
    """
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        # Find the item this comment belongs to
        item = get_object_or_404(Item, pk=self.kwargs['pk'])
        
        # Set the item and author before saving
        form.instance.item = item
        form.instance.author = self.request.user
        
        return super().form_valid(form)

    def get_success_url(self):
        # Redirect back to the item detail page
        return reverse('item_detail', kwargs={'pk': self.kwargs['pk']})


class ItemReportCreateView(LoginRequiredMixin, CreateView):
    """
    View for reporting a new item. Requires login.
    """
    model = Item
    form_class = ItemReportForm
    template_name = "portal/report_item.html"
    success_url = reverse_lazy("report_success")

    def form_valid(self, form):
        # Set the reporter to the currently logged-in user
        form.instance.reporter = self.request.user
        
        # Save the Item instance
        self.object = form.save()
        
        # Handle multiple image uploads
        images = self.request.FILES.getlist('images')
        for f in images:
            ItemImage.objects.create(item=self.object, image=f)
            
        return super().form_valid(form)
        
    def get_success_url(self):
        # We override this to redirect to a simple success page
        return reverse("report_success")

class ReportSuccessView(LoginRequiredMixin, TemplateView):
    """
    Displays a simple "success" message after an item is reported.
    """
    template_name = "portal/report_success.html"