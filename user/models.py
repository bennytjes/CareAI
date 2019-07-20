from django.db import models

# Create your models here.

class UserDetail(models.Model):
    Username = models.CharField(max_length = 20)
    Is_Supplier = models.BooleanField()
    First_Name = models.CharField(max_length = 20)
    Last_Name = models.CharField(max_length = 20)
    Organisation = models.CharField(max_length = 50)
    Town_City = models.CharField(max_length = 20)
    Post_Code = models.CharField(max_length = 10)
    Phone = models.IntegerField()
    Email = models.EmailField()

class UserAuth(models.Model):
    User_ID = models.OneToOneField(UserDetail,on_delete= models.CASCADE,primary_key = True)
    Password = models.CharField(max_length = 100)
    mobile = models.IntegerField()

class Products(models.Model):
    User_ID = models.ForeignKey(UserDetail,on_delete = models.CASCADE)
    Added_Date = models.DateField()
    Category = models.CharField(max_length = 30)
    Description = models.TextField()
