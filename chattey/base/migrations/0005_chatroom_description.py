# Generated by Django 4.1.12 on 2023-10-16 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_alter_message_receiver'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatroom',
            name='description',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
