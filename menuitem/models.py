from urllib import request
from django.db import models
import uuid
from django.contrib.auth import get_user_model
from account.models import Restaurant

User = get_user_model()


class MenuItem(models.Model):

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='menuitem', blank=True)
    stock = models.IntegerField()
    available = models.BooleanField(default=True)
    
    class Meta:
        ordering = ('name',)
        verbose_name = 'menuitem'
        verbose_name_plural = 'menuitems'

    def __str__(self):
        return self.name