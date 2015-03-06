from django.db import models

class UserQuery(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    query  = models.CharField(max_length=256)