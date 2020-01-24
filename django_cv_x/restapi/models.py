from django.db import models


# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=128, null=True, default="unknown")
    image = models.ImageField(upload_to="media/", max_length=256)
    score = models.FloatField("score of the classification", default=0.0, null=True)
