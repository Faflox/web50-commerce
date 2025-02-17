# Generated by Django 5.0.3 on 2024-04-06 15:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_alter_comment_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bid',
            name='listing',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='starting_price',
        ),
        migrations.AddField(
            model_name='listing',
            name='price',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bidPrice', to='auctions.bid'),
        ),
        migrations.AlterField(
            model_name='bid',
            name='price',
            field=models.FloatField(default=0.0),
        ),
    ]
