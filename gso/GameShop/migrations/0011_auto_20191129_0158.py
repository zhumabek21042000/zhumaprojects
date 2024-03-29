# Generated by Django 2.2.6 on 2019-11-28 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GameShop', '0010_auto_20191129_0118'),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='games',
            name='genres',
        ),
        migrations.AddField(
            model_name='games',
            name='genres',
            field=models.ManyToManyField(to='GameShop.Genre'),
        ),
    ]
