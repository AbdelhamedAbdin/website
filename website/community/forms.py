from django import forms
from .models import UserAsking, Comment
from django.forms import ValidationError


class UserAskingForm(forms.ModelForm):
    title = forms.CharField(required=True,
                            widget=forms.TextInput(attrs={'placeholder': 'Type Your Title...',
                                                          'class': 'form-control',
                                                          'data-placement': 'top',
                                                          'title': 'type your title',
                                                          'data-tooltip': 'tooltip'
                                                          }),
                            help_text='Be specific and imagine you’re asking a question to another person')
    question = forms.CharField(required=True,
                               widget=forms.Textarea(attrs={'placeholder': 'Type Your Details Of Your Question...',
                                                            'class': 'form-control',
                                                            'data-placement': 'top',
                                                            'title': 'type your question simply',
                                                            'data-tooltip': 'tooltip'
                                                            }),
                               help_text='Include all the information someone would need to answer your question')

    class Meta:
        model = UserAsking
        fields = '__all__'
        exclude = ['userprofile', 'ask_slug', 'likes', 'dislikes', 'favorite', 'clone_title']


class CommentForm(forms.ModelForm):
    comment = forms.CharField(max_length=500, required=False, widget=forms.Textarea(attrs={'placeholder': 'Type your comment simply',
                                                                                           'class': 'form-control'}))

    class Meta:
        model = Comment
        fields = ['comment']
