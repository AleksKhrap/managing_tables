# Generated by Django 4.2 on 2023-05-10 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('managing_tables', '0022_rename_looses_participant_defeats'),
    ]

    operations = [
        migrations.AlterField(
            model_name='table',
            name='logotype',
            field=models.ImageField(blank=True, upload_to='media'),
        ),
    ]