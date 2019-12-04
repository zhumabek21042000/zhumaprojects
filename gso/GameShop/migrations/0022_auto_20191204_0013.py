# Generated by Django 2.2.6 on 2019-12-03 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GameShop', '0021_auto_20191204_0013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='games',
            name='description',
            field=models.TextField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='games',
            name='game_rate',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
