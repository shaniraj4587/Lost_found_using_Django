from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django import forms

class CustomUserCreationForm(UserCreationForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("username", "email")  # Add 'email' to the form

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Change the label for 'username' to 'Roll No.'
        self.fields['username'].label = "Roll No."
        self.fields['username'].help_text = "Required. This will be your login ID."
        
        # Add Tailwind classes to all fields
        common_classes = "w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
        
        for fieldname, field in self.fields.items():
            field.widget.attrs.update({'class': common_classes})
            
            # Special handling for password help text
            if 'password' in fieldname:
                field.help_text = None