# Generated by Django 4.1 on 2022-08-11 23:47

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('drone', '0002_medication'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drone',
            name='drone_model',
            field=models.CharField(choices=[('Lightweight', 'heightweight'), ('Middleweight', 'middleweight'), ('Cruiserweight', 'cruiserweight'), ('Heavyweight', 'heavyweight')], default='Lightweight', help_text='model of the drone', max_length=100),
        ),
        migrations.CreateModel(
            name='LoadInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('drone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drone.drone')),
                ('medication', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drone.medication')),
            ],
        ),
    ]
