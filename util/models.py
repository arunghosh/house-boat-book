from django.db import models

from django.db import models


class BaseModel(models.Model):

    @property
    def is_new(self):
        return not self.id or self.id == 0

    class Meta:
        abstract = True


class AutoDateAddModel(BaseModel):
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True