from django.contrib import admin
from .models import Item, ItemImage, Comment

class ItemImageInline(admin.TabularInline):
    """
    Allows admins to add/edit ItemImages directly from the Item admin page.
    """
    model = ItemImage
    extra = 1  # Show 1 extra empty slot for uploading

@admin.action(description="Approve selected items")
def make_approved(modeladmin, request, queryset):
    """
    Admin action to approve items.
    """
    queryset.update(is_approved=True)

class ItemAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for the Item model.
    """
    list_display = ('title', 'item_type', 'reporter', 'reported_at', 'is_approved')
    list_filter = ('is_approved', 'item_type', 'reported_at')
    search_fields = ('title', 'description', 'location', 'reporter__username')
    actions = [make_approved]
    inlines = [ItemImageInline]  # Add the inline image editor

class CommentAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for the Comment model.
    """
    list_display = ('item', 'author', 'created_at', 'body')
    search_fields = ('body', 'author__username', 'item__title')
    list_filter = ('created_at',)

# Register your models with the custom admin classes
admin.site.register(Item, ItemAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(ItemImage) # Optional: manage images separately