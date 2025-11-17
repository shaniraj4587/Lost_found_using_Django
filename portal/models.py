from django.db import models
from django.conf import settings
from django.utils import timezone
import os

def get_image_upload_path(instance, filename):
    """
    Generates a custom upload path for ItemImage.
    Renames file to: `media/item_images/{roll_no}_{datetime}.{ext}`
    """
    # Get the roll_no from the related Item's reporter
    roll_no = instance.item.reporter.username
    # Get current datetime
    now = timezone.now()
    datetime_str = now.strftime("%Y%m%d_%H%M%S")
    # Get file extension
    ext = os.path.splitext(filename)[1]
    # Combine them
    return f"item_images/{roll_no}_{datetime_str}{ext}"


class Item(models.Model):
    """
    Represents a single lost or found item.
    """
    ITEM_TYPES = (
        ('lost', 'Lost Item'),
        ('found', 'Found Item'),
    )
    
    item_type = models.CharField(max_length=5, choices=ITEM_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200, help_text="Where did you lose/find it?")
    reported_at = models.DateTimeField(auto_now_add=True)
    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    
    # Admin approval field
    is_approved = models.BooleanField(
        default=False,
        help_text="Designates whether this item is approved and visible on the site."
    )

    def __str__(self):
        return f"[{self.get_item_type_display()}] {self.title} by {self.reporter.username}"

    def get_first_image_url(self):
        """
        Gets the URL of the first image for this item, or a placeholder.
        """
        first_image = self.images.first()
        if first_image:
            return first_image.image.url
        return "https://placehold.co/600x400/eeeeee/cccccc?text=No+Image"


class ItemImage(models.Model):
    """
    Represents one image associated with a reported Item.
    This allows for multiple images per item.
    """
    item = models.ForeignKey(
        Item,
        related_name='images',
        on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to=get_image_upload_path)

    def __str__(self):
        return f"Image for {self.item.title}"


class Comment(models.Model):
    """
    Represents a comment on a specific Item.
    """
    item = models.ForeignKey(
        Item,
        related_name='comments',
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.author.username} on {self.item.title}"