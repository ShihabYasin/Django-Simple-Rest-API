from django.db import models

class ItemModel (models.Model):
    id = models.IntegerField (primary_key=True)
    name = models.CharField (max_length=80, blank=False, editable=True)
    price = models.IntegerField(editable=True, default=0)

    class Meta:
        ordering = ('id',)

    # def __str__(self):
    #     return f"{self.name}:{self.price}"
