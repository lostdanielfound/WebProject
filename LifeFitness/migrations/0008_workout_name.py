# Generated by Django 4.1.1 on 2022-11-21 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LifeFitness', '0007_exercise_workout_workoutreport'),
    ]

    operations = [
        migrations.AddField(
            model_name='workout',
            name='name',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
