from django.db import models
from user.models import Products

# Create your models here.
class Questions(models.Model):
    description = models.TextField()
    in_principle = models.IntegerField()

class Versions(models.Model):
    online_date = models.DateField()


class VersionToQuestion(models.Model):
    version_id = models.ForeignKey(Versions,on_delete= models.CASCADE)
    question_id = models.ForeignKey(Questions,on_delete= models.CASCADE)
    class Meta:
        unique_together = ('version_id','question_id')

class Entries(models.Model):
    product_id = models.ForeignKey(Products,on_delete= models.CASCADE)
    version_id = models.ForeignKey(Versions,on_delete = models.CASCADE)
    entry_time = models.DateTimeField()
    principle = models.IntegerField()
    jotform_submission_id = models.CharField(max_length = 30)
    score = models.FloatField(null = True, default = 0)

class Answers(models.Model):
    entry_id = models.ForeignKey(Entries,on_delete=models.CASCADE)
    question_id = models.ForeignKey(Questions,on_delete = models.CASCADE)
    answers = models.TextField()

class JotFormIDs(models.Model):
    principle = models.IntegerField()
    jotform_id = models.CharField(max_length = 30)

    