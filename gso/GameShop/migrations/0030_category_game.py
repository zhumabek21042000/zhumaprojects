# Generated by Django 2.2.6 on 2019-12-07 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GameShop', '0029_remove_category_game'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='game',
            field=models.ManyToManyField(blank=True, null=True, to='GameShop.Games'),
        ),
    ]
