from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    first_name= forms.CharField(label='Име',max_length=30,required=True)
    last_name= forms.CharField(label='Фамилия',max_length=50,required=True)
    email = forms.EmailField(required=True, label="Имейл адрес")

    class Meta:
        model = User
        fields = ['first_name','last_name','username', 'email', 'password1', 'password2']
        labels = {
            'username': 'Потребителско име',
            'password1': 'Парола',
            'password2': 'Потвърди паролата',
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Този имейл вече е регистриран.")
        return email



class LoginForm(forms.Form):
    username = forms.CharField(label='Потребителско име', max_length=150, widget=forms.TextInput(attrs={
        'placeholder': 'Потребителско име',
        'class': 'form-control'
    }))
    password = forms.CharField(label='Парола', widget=forms.PasswordInput(attrs={
        'placeholder': 'Парола',
        'class': 'form-control'
    }))
