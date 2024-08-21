from django.db import models

# Create your models here.
class News(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    date = models.DateField()
    genre = models.CharField(blank=True, max_length=250)
    year = models.IntegerField(blank=True, null=True)


    def __str__(self): return self.title