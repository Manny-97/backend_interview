from django.db import models
from django.db.models.signals import pre_save
from django.db.utils import OperationalError
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Drone(models.Model):

    serial_number = models.CharField(
        max_length=100,
        unique=True,
        help_text='serial number of the drone'
    )

    DRONE_MODEL = [
        ('Lightweight', 'heightweight'), 
        ('Middleweight', 'middleweight'), 
        ('Cruiserweight', 'cruiserweight'), 
        ('Heavyweight', 'heavyweight')
    ]

    drone_model = models.CharField(
        choices=DRONE_MODEL,
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
        validators=[MaxValueValidator(100), MinValueValidator(0)],
        default=100,
        help_text=''
    )

    DRONE_STATE = [
        ('IDLE', 'idle'), 
        ('LOADING', 'loading'), 
        ('LOADED', 'loaded'), 
        ('DELIVERING', 'delivering'), 
        ('DELIVERED', 'delivered'), 
        ('RETURNING', 'returning')
        ]
    state = models.CharField(
        max_length=20,
        choices=DRONE_STATE,
        default='IDLE',
        help_text='statof the dronr'
    )

    