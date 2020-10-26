from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordResetForm
from django import forms
from django.contrib.auth.models import User
from .models import UserProfile


# UserCreationForm
class SignUp(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ['username',
                  'first_name',
                  'last_name',
                  'password1',
                  'password2',
                  'email']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('username is already exists')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('email is already exists')
        return email


# Set attribute on email field
class ResetPassword(PasswordResetForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email address',
                                                                           'class': 'form-control'}))


# Edit your data except password
class EditForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def edit(self):
        user = super(EditForm, self).save(commit=False)

        if user.commit:
            user.save()
        return user


# Add new logo and replace it with old logo
class UpdateAvatarForm(forms.ModelForm):
    pass

    class Meta:
        model = UserProfile
        fields = ['logo']


class UpdateInfoForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = '__all__'
        exclude = ['user', 'logo', 'slug']