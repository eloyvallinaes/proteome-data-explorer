# Generated by Django 3.2 on 2021-11-09 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('explore', '0011_rename_id_props__id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='props',
            name='_id',
        ),
        migrations.AddField(
            model_name='props',
            name='id',
            field=models.BigAutoField(auto_created=True, default=0, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]
