# Generated by Django 5.0.2 on 2024-02-21 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('volunteers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='volunteer',
            name='order_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='volunteer',
            name='volunteer_role',
            field=models.CharField(choices=[('board member', 'BOARDMEMBER'), ('coach', 'COACH'), ('manager', 'MANAGER'), ('scorekeeper', 'SCOREKEEPER'), ('umpire', 'UMPIRE')], default='umpire', max_length=12),
        ),
    ]