# Generated by Django 3.2 on 2021-11-09 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('explore', '0013_alter_props_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='props',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
