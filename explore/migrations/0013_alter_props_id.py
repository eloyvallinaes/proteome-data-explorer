# Generated by Django 3.2 on 2021-11-09 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('explore', '0012_auto_20211109_1111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='props',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]