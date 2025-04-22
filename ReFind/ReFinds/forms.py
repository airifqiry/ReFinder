from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Ad


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        label="Име",
        widget=forms.TextInput(attrs={'placeholder': 'Име', 'class': 'form-control'})
    )
    last_name = forms.CharField(
        label="Фамилия",
        widget=forms.TextInput(attrs={'placeholder': 'Фамилия', 'class': 'form-control'})
    )
    username = forms.CharField(
        label="Потребителско име",
        widget=forms.TextInput(attrs={'placeholder': 'Потребителско име', 'class': 'form-control'})
    )
    email = forms.EmailField(
        label="Имейл",
        widget=forms.EmailInput(attrs={'placeholder': 'Имейл адрес', 'class': 'form-control'})
    )
    password1 = forms.CharField(
        label="Парола",
        widget=forms.PasswordInput(attrs={'placeholder': 'Парола', 'class': 'form-control'})
    )
    password2 = forms.CharField(
        label="Потвърди парола",
        widget=forms.PasswordInput(attrs={'placeholder': 'Потвърди парола', 'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']




class LoginForm(forms.Form):
    username = forms.CharField(label='Потребителско име', max_length=150, widget=forms.TextInput(attrs={
        'placeholder': 'Потребителско име',
        'class': 'form-control'
    }))
    password = forms.CharField(label='Парола', widget=forms.PasswordInput(attrs={
        'placeholder': 'Парола',
        'class': 'form-control'
    }))



class ImageSearchForm(forms.Form):
    image = forms.ImageField(label="Качи снимка")





class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['image', 'title','status', 'description', 'location', 'latitude', 'longitude']

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if description and len(description.split()) > 50:
            raise forms.ValidationError("Описанието не трябва да надвишава 50 думи.")
        return description

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image and image.size > 5 * 1024 * 1024:
            raise forms.ValidationError("Снимката трябва да е под 5MB.")
        return image

