from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.utils import timezone
from multiselectfield import MultiSelectField

# Create your models here.

class UserDetails(models.Model):
    user_id = models.OneToOneField(User,on_delete = models.CASCADE,primary_key = True,default=0,db_column='user_id')
    username = models.CharField(max_length = 50,null=True)
    is_supplier = models.BooleanField(default = False,verbose_name = 'I am a supplier')
    first_name = models.CharField(max_length = 20,null=True)
    last_name = models.CharField(max_length = 20,null=True)
    organisation = models.CharField(max_length = 50,null=True)
    town_city = models.CharField(max_length = 20,null=True)
    post_code = models.CharField(max_length = 10,null=True)
    phone = models.CharField(max_length = 20,null=True)



CATEGORY_CHOICES = (('Diagnostic','Diagnostic'),
                        ('Therapeutic','Therapeutic'),
                        ('Population health','Population health'),
                        ('Care-based','Care-based'),
                        ('Triage','Triage'),
                        ('Self-care','Self-care'),
                        ('Health promotion','Health promotion'),
                        ('Remote Monitoring','Remote Monitoring'),
                        ('Remote Consultation','Remote Consultation'),
                        ('Other','Other (please specify)'))
DEPLOY_POINT_CHOICES = (('Primary Care','Primary Care'),
                        ('Secondary Care','Secondary Care'),
                        ('Community Care','Community Care'),
                        ('Tertiary Care','Tertiary Care'),
                        ('Individual Care of Self e.g. user’s home/office','Individual Care of Self e.g. user’s home/office'),
                        ('For the purposes of population screening','For the purposes of population screening'),
                        ('Other','Other (please specify)'))


class Products(models.Model):
    product_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User,on_delete = models.CASCADE,db_column='user_id')
    product_name = models.CharField(max_length = 100,default = 'product name')
    added_date = models.DateField(default=timezone.now().date())
    category = models.CharField(max_length = 30,choices = CATEGORY_CHOICES)
    other_category = models.CharField(max_length = 30,blank=True, null = True,verbose_name='Other category:')
    deploy_point = MultiSelectField(max_length= 100,choices=DEPLOY_POINT_CHOICES, default = 'other', 
    verbose_name='At which point of care do you expect your data-driven solution to be deployed? Select as many as applicable.')
    other_deploy_point = models.CharField(max_length = 100,blank = True, null = True,verbose_name = 'Other point of care:')
    description = models.TextField()

class Scores(models.Model):
    product_id = models.OneToOneField(Products,primary_key = True,on_delete= models.CASCADE)
    principle_1 = models.FloatField(default=0)
    principle_2 = models.FloatField(default=0)
    principle_3 = models.FloatField(default=0)
    principle_4 = models.FloatField(default=0)
    principle_5 = models.FloatField(default=0)
    principle_6 = models.FloatField(default=0)
    principle_7 = models.FloatField(default=0)
    principle_8 = models.FloatField(default=0)
    principle_9 = models.FloatField(default=0)
    principle_10 = models.FloatField(default=0)

    