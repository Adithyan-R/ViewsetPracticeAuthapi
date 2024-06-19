from django.db import models

# Create your models here.

class Tutorial(models.Model):
    tutorialNo = models.IntegerField()
    title = models.CharField(max_length=100)
    content = models.TextField()


