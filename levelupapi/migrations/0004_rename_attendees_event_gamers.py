# Generated by Django 4.0.4 on 2022-05-02 18:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('levelupapi', '0003_alter_event_attendees'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='attendees',
            new_name='gamers',
        ),
    ]
