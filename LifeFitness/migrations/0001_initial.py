# Generated by Django 4.1.2 on 2022-11-23 18:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Workout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, max_length=300)),
                ('repCount', models.IntegerField(default=0)),
                ('setCount', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Workout_Session',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200)),
                ('date', models.DateField(auto_now=True)),
                ('exerciseList', models.ManyToManyField(to='LifeFitness.workout')),
                ('fitnesuser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Workout_Session_Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('self_report', models.TextField(blank=True, max_length=300)),
                ('duration', models.TimeField()),
                ('workoutID', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='LifeFitness.workout_session')),
            ],
        ),
        migrations.CreateModel(
            name='FitnessProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currentheight', models.IntegerField(default=0)),
                ('currentWeight', models.IntegerField(default=0)),
                ('BMI', models.IntegerField(default=0)),
                ('goalWeight', models.IntegerField(default=0)),
                ('fitnessUser', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
