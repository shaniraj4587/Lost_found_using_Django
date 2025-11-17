from django import forms
from .models import Item, Comment

class ItemReportForm(forms.ModelForm):
    """
    Form for reporting a new Lost or Found Item.
    NOTE: The multiple image upload is handled directly in the template,
    not as a field here, to avoid the ValueError.
    """
    class Meta:
        model = Item
        fields = ['item_type', 'title', 'description', 'location']
        widgets = {
            'item_type': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add Tailwind classes to all fields
        common_classes = "w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
        
        for fieldname, field in self.fields.items():
            if fieldname != 'item_type': # item_type already styled
                field.widget.attrs.update({'class': common_classes})

class CommentForm(forms.ModelForm):
    """
    Form for adding a comment to an item.
    """
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(
                attrs={
                    'rows': 3,
                    'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500',
                    'placeholder': 'Write your comment...'
                }
            )
        }
        labels = {
            'body': ''  # Hide the label
        }