# Generated by Django 2.2.6 on 2019-12-02 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GameShop', '0016_remove_profile_balance'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='balance',
            field=models.FloatField(default=0),
        ),
    ]