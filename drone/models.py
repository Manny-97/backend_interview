from tkinter import CASCADE
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db.utils import OperationalError
from .utils import validate_size
from django.db.models.signals import pre_save
from django.dispatch import receiver

# Create your models here.
class Drone(models.Model):

    serial_number = models.CharField(
        max_length=100,
        unique=True,
        help_text='serial number of the drone'
    )

    DRONE_MODEL = [
        ('Lightweight', 'Leightweight'), 
        ('Middleweight', 'Middleweight'), 
        ('Cruiserweight', 'Cruiserweight'), 
        ('Heavyweight', 'Heavyweight')
    ]

    drone_model = models.CharField(
        choices=DRONE_MODEL,
        max_length=100,
        default='Lightweight',
        help_text="model of the drone"
    )
    weight_limit = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MaxValueValidator(500, "The maximum weight that can be carried is 500g"), 
        MinValueValidator(1, "The minimum weight to load a drone with is 1g")],
        help_text='weight of medication to be loaded in grammes'
    )
    battery_capacity = models.PositiveIntegerField(
        validators=[MaxValueValidator(100), MinValueValidator(0)],
        default=100,
        help_text="Battery's current capacity. Ranges from 0% to 100%"
    )

    DRONE_STATE = [
        ('IDLE', 'Idle'), 
        ('LOADING', 'Loading'), 
        ('LOADED', 'Loaded'), 
        ('DELIVERING', 'Delivering'), 
        ('DELIVERED', 'Delivered'), 
        ('RETURNING', 'Returning')
        ]
    state = models.CharField(
        max_length=20,
        choices=DRONE_STATE,
        default='IDLE',
        help_text='state of the drone'
    )

    def __str__(self):
        return f"{self.serial_number} {self.drone_model} - capacity: {self.weight_limit}"

@receiver(pre_save, sender=Drone)   
def drone_validator(sender, instance, *args, **kwargs):
    validate_size(Drone, OperationalError)


class Medication(models.Model):

    name = models.CharField(
        validators=[RegexValidator(r"^[a-zA-Z0-9-_]+$", "Allowed only letters, numbers, -, _")],
        max_length=150,
        unique=True,
        help_text='name of medicine or medication'
    )
    weight = models.DecimalField(
        validators=[MinValueValidator(1)],
        max_digits=5,
        decimal_places=2,
        help_text='weight of medication in grammes'
    )
    code = models.CharField(
        validators=[RegexValidator(r"^[A-Z0-9_]+$", "Allowed only upper case letters, underscore and numbers")],
        max_length=150,
        unique=True,
        help_text='code on the medication'
    )
    image = models.ImageField(
        upload_to='images/'

    )

    def __str__(self) -> str:
        return f"Medicine: {self.name}, Code: {self.code} - Capacity: {self.weight}"


class LoadInformation(models.Model):

    drone = models.ForeignKey('Drone', on_delete=models.CASCADE)
    medication = models.ForeignKey('Medication', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    def __str__(self) -> str:
        return f"Drone: {self.drone}, Medication: {self.medication}, Quantity: {self.quantity}"