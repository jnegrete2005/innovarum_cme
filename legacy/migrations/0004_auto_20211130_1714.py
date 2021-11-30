# Generated by Django 3.2.8 on 2021-11-30 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('legacy', '0003_auto_20211130_1659'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userquiz',
            name='score',
        ),
        migrations.AddField(
            model_name='userquiz',
            name='score',
            field=models.ManyToManyField(related_name='answered', to='legacy.Answer'),
        ),
    ]
