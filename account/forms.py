from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class RegistrationForm(UserCreationForm):

    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for field in (self.fields['first_name'], self.fields['last_name'], self.fields['username'], self.fields['password1'], self.fields['password2']):
            field.widget.attrs.update({'class': 'shadow appearance-none border rounded w-full py-1.5 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'})
    
    class Meta:
        model = User
        fields = ('first_name','last_name','username','password1','password2')


class LoginForm(forms.ModelForm):

    password  = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model  =  User
        fields =  ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for field in (self.fields['username'],self.fields['password']):
            field.widget.attrs.update({'class': 'shadow appearance-none border rounded w-full py-1.5 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'})

    def clean(self):
        if self.is_valid():
            username = self.cleaned_data.get('username')
            password = self.cleaned_data.get('password')
            if not authenticate(username=username, password=password):
                raise forms.ValidationError(_('Invalid Credentials.'))