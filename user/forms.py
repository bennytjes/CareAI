from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserDetail, Products
from datetime import date


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    # is_supplier = forms.BooleanField()

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2'
        )

    def save(self, commit = True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data.get('email')

        if commit:
            user.save()

        return user    

class UserDetailForm(forms.ModelForm):
    class Meta:
        model= UserDetail
        fields = [
            'username',
            'is_supplier',
            'first_name',
            'last_name',
            'organisation',
            'town_city',
            'post_code',
            'phone',
        ]
        widgets = {
            'username': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

class ProductsRegisterForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = [
            'product_name',
            'added_date',
            'category',
            'description',
        ]
        widgets = {
            'added_date':  forms.TextInput(attrs={'readonly': 'readonly'}),
        }