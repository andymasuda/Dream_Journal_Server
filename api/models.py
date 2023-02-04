from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Entry(models.Model):
    title = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # created_by = models.ForeignKey(User, on_delete=models.CASCADE)

