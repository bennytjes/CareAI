from django.test import TestCase,Client
from django.urls import reverse
from user.models import UserDetails,Products,Scores
import json
from django.contrib.auth.models import User

class Test_User_Views(TestCase):
    def setUp(self):
        self.client = Client()
        self.test_user = User.objects.create_user(username='testuser', password='djangodjango')
        self.test_user.save()
        self.test_product = Products(user_id = self.test_user,product_name = 'testproduct',category='Other',deploy_point = 'Other',description = 'test')
        self.test_product.save()
        self.client.login(username='testuser',password = 'djangodjango')
        self.test_userdetail= UserDetails(user_id = self.test_user,username = 'testuser',is_supplier=False)
        self.test_userdetail.save()

    def test_register_GET(self):
        response = self.client.get(reverse('user:register'))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'reg_form.html')

    def test_change_password_GET(self):
        response = self.client.get(reverse('user:change_password'))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'change_password.html')
    
    def test_change_password_POST(self):
        response = self.client.post('/user/change_password/',{'old_password': 'djangodjango','new_password1':'superdjango','new_password2':'superdjango'})
        self.assertEquals(response.status_code,302)
        self.assertEquals(response.url,"/user/profile/")

    def test_profile_GET(self):
        response = self.client.get(reverse('user:profile'))
        self.assertEquals(response.status_code,302)

    def test_profile_edit_GET(self):
        response = self.client.get(reverse('user:profile_edit'))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'profile_edit.html')

    def test_profile_edit_POST(self):
        response = self.client.get('/user/profile/edit/',{'first_name':'John'})
        self.assertEquals(response.status_code,200)
    
    def test_products_GET(self):
        response = self.client.get(reverse('user:products'))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'products.html')

    def test_products_register_GET(self):
        response = self.client.get(reverse('user:products_register'))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'products_register.html')

    def test_products_register_POST(self):
        response = self.client.post('/user/products/register/',{'product_name':'new test product'})
        self.assertEquals(response.status_code,200)

    def test_products_edit_GET(self):
        response = self.client.get(reverse('user:product_edit',args = [self.test_product.pk])) 
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'product_edit.html')
    
    def test_products_edit_POST(self):
        response = self.client.post('/user/products/'+str(self.test_product.pk),{'product_name':'another test name'})
        self.assertEquals(response.status_code,200)


