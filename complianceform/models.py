from django.db import models
from user.models import Products

# Create your models here.
class Questions(models.Model):

    Description = models.TextField()
    In_Principle = models.IntegerField()


class Version(models.Model):
    Online_Date = models.DateField()


class Version_Question(models.Model):
    Version_ID = models.ForeignKey(Version,on_delete= models.CASCADE)
    Question_ID = models.ForeignKey(Questions,on_delete= models.CASCADE)
    class Meta:
        unique_together = ('Version_ID','Question_ID')

class Entry(models.Model):
    Product_ID = models.ForeignKey(Products,on_delete= models.CASCADE)
    Version_ID = models.ForeignKey(Version,on_delete = models.CASCADE)
    Entry_time = models.DateTimeField()

class Answers(models.Model):
    Entry_ID = models.ForeignKey(Entry,on_delete=models.CASCADE)
    Question_ID = models.ForeignKey(Questions,on_delete = models.CASCADE)
    Answers = models.TextField()
