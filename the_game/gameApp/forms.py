from django import forms
from django.contrib.auth.models import User

#used forms.ModelForm to create registration form regarding User model

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True

    class Meta():
        model = User
        fields = ('username','email','password' )
