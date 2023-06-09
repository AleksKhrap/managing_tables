# Generated by Django 4.2 on 2023-05-03 11:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('managing_tables', '0010_delete_participant'),
    ]

    operations = [
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('participant', models.CharField(max_length=50)),
                ('wins', models.PositiveSmallIntegerField(blank=True, default=0)),
                ('draws', models.PositiveSmallIntegerField(blank=True, default=0)),
                ('looses', models.PositiveSmallIntegerField(blank=True, default=0)),
                ('total_games', models.PositiveSmallIntegerField(blank=True, default=0)),
                ('points', models.PositiveSmallIntegerField(blank=True, default=0)),
                ('table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='managing_tables.table')),
            ],
        ),
    ]
