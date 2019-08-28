from django.test import SimpleTestCase
from django.urls import reverse, resolve
from user.views import *
from django.contrib.auth.views import LoginView,LogoutView
from user.models import Products

class Test_User_Urls(SimpleTestCase):
    def test_login(self):
        url = reverse('user:login')
        self.assertEquals(resolve(url).func.view_class,LoginView)
        self.testProduct = Products()
    
    def test_logout(self):
        url = reverse('user:logout')
        self.assertEquals(resolve(url).func.view_class,LogoutView)

    def test_register(self):
        url = reverse('user:register')
        self.assertEquals(resolve(url).func,register)

    def test_change_password(self):
        url = reverse('user:change_password')
        self.assertEquals(resolve(url).func,change_password)
    
    def test_profile(self):
        url = reverse('user:profile')
        self.assertEquals(resolve(url).func,profile) 
    
    def test_profile_edit(self):
        url = reverse('user:profile_edit')
        self.assertEquals(resolve(url).func,profile_edit)

    def test_products(self):
        url = reverse('user:products')
        self.assertEquals(resolve(url).func,products)  

    def test_products_register(self):
        url = reverse('user:products_register')
        self.assertEquals(resolve(url).func,products_register)      

    def test_products_edit(self):
        url = reverse('user:product_edit', args = [12])
        self.assertEquals(resolve(url).func,product_edit)       

    