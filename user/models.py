from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.utils import timezone
# Create your models here.

class UserDetail(models.Model):
    user_id = models.OneToOneField(User,on_delete = models.CASCADE,primary_key = True,default=0,db_column='user_id')
    username = models.CharField(max_length = 50)
    is_supplier = models.BooleanField(default = False)
    first_name = models.CharField(max_length = 20,null=True)
    last_name = models.CharField(max_length = 20,null=True)
    organisation = models.CharField(max_length = 50,null=True)
    town_city = models.CharField(max_length = 20,null=True)
    post_code = models.CharField(max_length = 10,null=True)
    phone = models.CharField(max_length = 20,null=True)


class Products(models.Model):
    user_id = models.ForeignKey(User,on_delete = models.CASCADE)
    product_name = models.CharField(max_length = 100,default = 'product name')
    added_date = models.DateField(default=timezone.now().date())
    category = models.CharField(max_length = 30)
    description = models.TextField()
