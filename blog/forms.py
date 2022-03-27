from socket import fromshare
from django import forms

from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ["post"]
        labels = {
            "user_name": "Name",
            "user_email": "Email",
            "text": "Comment"
        }