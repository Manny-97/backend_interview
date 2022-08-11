from django.db import models
from django.db.models.signals import pre_save
from django.db.utils import OperationalError
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Drone(models.Model):

    MODEL = [
        ('Lightweight', 'heightweight'), 
        ('Middleweight', 'middleweight'), 
        ('Cruiserweight', 'cruiserweight'), 
        ('Heavyweight', 'heavyweight')
    ]

    drone_model = models.CharField(
        choices=MODEL,
        max_length=100,
        help_text="model of the drone"
    )
    weight_limit = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MaxValueValidator(500, "The maximum weight that can be carried is 500g"), 
        MinValueValidator(1, "The minimum weight to load a drone with is 1g")]
    )
    battery_capacity = models.PositiveIntegerField(
        default=100
    )