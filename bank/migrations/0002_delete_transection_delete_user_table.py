# Generated by Django 4.2.3 on 2023-08-22 11:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Transection',
        ),
        migrations.DeleteModel(
            name='User_table',
        ),
    ]