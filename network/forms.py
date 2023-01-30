from django.forms import ModelForm
from .models import *
from django import forms

class NewPost(forms.Form):
    tekst = forms.CharField(widget=forms.Textarea)

class Newpost1(ModelForm):
    class Meta:
        model = Postovi
        fields = ['title','post1']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'text-center form-control', 'placeholder':"Input your title here"}),
            'post1': forms.Textarea(attrs={'class': 'text-center form-control', 'placeholder':"Input your text post here"}),
        }
        labels = {
            'title': "",
            'post1': ""
        }
class CommentForm(ModelForm):
    class Meta:
        model = Komentar
        fields = ['comment']
        widgets = {
            'comment':forms.TextInput(attrs={'class': 'form-control', 'placeholder':"Enter your comment here",}),
        }
        labels = {
            'comment': "",
        }
