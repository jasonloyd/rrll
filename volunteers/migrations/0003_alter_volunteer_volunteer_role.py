# Generated by Django 5.0.2 on 2024-02-21 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('volunteers', '0002_volunteer_order_id_volunteer_volunteer_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='volunteer',
            name='volunteer_role',
            field=models.CharField(choices=[('BOARDMEMBER', 'board member'), ('COACH', 'coach'), ('MANAGER', 'manager'), ('SCOREKEEPER', 'scorekeeper'), ('UMPIRE', 'umpire')], default='UMPIRE', max_length=12),
        ),
    ]
