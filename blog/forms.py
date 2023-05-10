from django import forms
from django.contrib.auth import authenticate
from .models import *



class ContactForm(forms.Form):
    name = forms.CharField(max_length=255)
    email = forms.EmailField()
    address = forms.CharField(widget=forms.TextInput)
    message = forms.CharField(widget=forms.Textarea)

class SignupForm(forms.Form):
    username = forms.CharField(max_length=255)
    email = forms.EmailField()
    password1=forms.CharField(widget=forms.PasswordInput())
    password2=forms.CharField(widget=forms.PasswordInput())

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 !=password2:
            raise forms.ValidationError("password didnt match")
        return password2
    
class LoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username,password=password)

        if not user:
            raise forms.ValidationError('Incorrect error')
        return  self.cleaned_data


class Addpost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['author','title','content','image']