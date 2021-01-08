from django.db import models
from django.utils import timezone
import uuid

# Create your models here.
class ShoppingItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    userID = models.CharField(max_length = 100)
    itemName = models.CharField(max_length = 100)
    quantityItem = models.IntegerField()
    status = models.CharField(max_length = 50)
    date = models.DateField(default = timezone.now)