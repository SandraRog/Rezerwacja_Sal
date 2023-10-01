# Generated by Django 4.2.5 on 2023-09-29 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('room_capacity', models.IntegerField()),
                ('projector_availability', models.BooleanField(default=False)),
            ],
        ),
    ]
