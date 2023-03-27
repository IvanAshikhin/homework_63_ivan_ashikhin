from django import forms

from posts.models import Post, Comment


class SearchForm(forms.Form):
    search = forms.CharField(max_length=20, required=False, label='Find')


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['description', 'image']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        labels = {
            'text': 'Your comment',
        }