from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserDetails, Products
from datetime import date

#Custom registration form which only takes username, email and password
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

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

#Custom user detail model form from the UserDetails model
#With username as read only field
class UserDetailForm(forms.ModelForm):
    class Meta:
        model= UserDetails
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

#Custom product form from the Products model
#With added_date as read only field and deploy_point as a multiple checkbox field.
class ProductsRegisterForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = [
            'product_name',
            'added_date',
            'category',
            'other_category',
            'deploy_point',
            'other_deploy_point',
            'description',
        ]
        widgets = {
            'added_date':  forms.TextInput(attrs={'readonly': 'readonly'}),
            'deploy_point': forms.CheckboxSelectMultiple(),
            
        }