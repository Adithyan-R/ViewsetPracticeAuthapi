from django.db import models
from django.db.models import CASCADE


# Create your models here.

class Tutorial(models.Model):
    tutorialNo = models.IntegerField()
    title = models.CharField(max_length=100)
    content = models.TextField()

class Comment(models.Model):
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE)
    content = models.TextField()
    author = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)






'''
class Duration(models.Model):
    tutorialNo = models.ForeignKey(Tutorial,on_delete=CASCADE)
    startDate = models.DateField(auto_now_add=True)
    status = models.DurationField()
'''