# Generated by Django 5.0.2 on 2024-02-26 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='addr_type',
            field=models.CharField(choices=[('RESIDENCE', 'R'), ('PERMANENT', 'P'), ('COMMUNICATION', 'C')], default='RESIDENCE'),
        ),
    ]
