# Generated by Django 5.0.3 on 2024-03-21 10:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_alter_comment_text_alter_listing_description_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='user',
        ),
    ]
