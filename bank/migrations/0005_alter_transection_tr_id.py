# Generated by Django 4.2.3 on 2023-08-22 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0004_alter_transection_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transection',
            name='tr_id',
            field=models.CharField(max_length=30),
        ),
    ]
