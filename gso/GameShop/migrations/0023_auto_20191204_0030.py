# Generated by Django 2.2.6 on 2019-12-03 18:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('GameShop', '0022_auto_20191204_0013'),
    ]

    operations = [
        migrations.RenameField(
            model_name='news',
            old_name='user',
            new_name='author',
        ),
    ]