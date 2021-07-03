from django import forms
from .models import Comment
from .models import post





class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Text goes here', 'rows': '4', 'cols': '10'}))

    class Meta:
        model = Comment
        fields = ('content',)


class UploadForm(forms.ModelForm):
    class Meta:
        model = post
        fields = ('image', 'video', 'content',)















