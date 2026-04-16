from django import forms
from users.models import User
from django.contrib.auth.forms import UserCreationForm

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'role',
            'password1',
            'password2'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(self.fields.keys())
        # 🔥 Add Bootstrap class to all fields
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'})
        )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
        )