from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from quiz.models import Users, Questions


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class utiliForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['type']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Questions
        fields = ['question','optiona','optionb','optionc','optiond','answer','catagory']

class LoginForm(forms.Form):

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data["username"]
        password = self.cleaned_data["password"]

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("This is user does not exist")
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect password")
            if not user.is_superuser:
                raise forms.ValidationError("This user is not longer active")
        return super(LoginForm, self).clean(*args, *kwargs)