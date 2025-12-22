from django.db import models

# Create your models here.

class UniqueItem(models.Model):
    name = models.CharField(max_length=20)
    buffer = models.IntegerField(default=0)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    