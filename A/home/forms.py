from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model= Comment
        fields= ['body']
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'width: 100%; padding: 10px; border-radius: 10px; border: 1px solid #ccc;',
                'rows': 4,
            })
        }

class ReplyForm(forms.Form):
    reply=forms.TimeField(widget=forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your reply here...',
                'rows': 3}))






