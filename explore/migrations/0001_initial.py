# Generated by Django 3.0.8 on 2021-05-27 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Props',
            fields=[
                ('Name', models.TextField(db_column='Name', primary_key=True, serialize=False)),
                ('Length', models.FloatField(blank=True, db_column='Length', null=True)),
                ('Mass', models.FloatField(blank=True, db_column='Mass', null=True)),
                ('SASAmiller', models.FloatField(blank=True, db_column='SASAmiller', null=True)),
                ('NetCh', models.FloatField(blank=True, db_column='NetCh', null=True)),
                ('NCD', models.FloatField(blank=True, db_column='NCD', null=True)),
                ('fFatty', models.FloatField(blank=True, db_column='fFatty', null=True)),
                ('fPos', models.FloatField(blank=True, db_column='fPos', null=True)),
                ('fNeg', models.FloatField(blank=True, db_column='fNeg', null=True)),
                ('GC', models.FloatField(blank=True, db_column='GC', null=True)),
                ('seqnum', models.FloatField(blank=True, db_column='SeqNum', null=True)),
                ('fCharged', models.FloatField(blank=True, db_column='fCharged', null=True)),
                ('ncd1000', models.FloatField(blank=True, db_column='NCD1000', null=True)),
                ('mwkda', models.FloatField(blank=True, db_column='MWkDa', null=True)),
                ('i', models.FloatField(blank=True, db_column='I', null=True)),
                ('l', models.FloatField(blank=True, db_column='L', null=True)),
                ('v', models.FloatField(blank=True, db_column='V', null=True)),
                ('a', models.FloatField(blank=True, db_column='A', null=True)),
                ('g', models.FloatField(blank=True, db_column='G', null=True)),
                ('p', models.FloatField(blank=True, db_column='P', null=True)),
                ('f', models.FloatField(blank=True, db_column='F', null=True)),
                ('m', models.FloatField(blank=True, db_column='M', null=True)),
                ('w', models.FloatField(blank=True, db_column='W', null=True)),
                ('y', models.FloatField(blank=True, db_column='Y', null=True)),
                ('h', models.FloatField(blank=True, db_column='H', null=True)),
                ('t', models.FloatField(blank=True, db_column='T', null=True)),
                ('s', models.FloatField(blank=True, db_column='S', null=True)),
                ('n', models.FloatField(blank=True, db_column='N', null=True)),
                ('q', models.FloatField(blank=True, db_column='Q', null=True)),
                ('d', models.FloatField(blank=True, db_column='D', null=True)),
                ('e', models.FloatField(blank=True, db_column='E', null=True)),
                ('k', models.FloatField(blank=True, db_column='K', null=True)),
                ('r', models.FloatField(blank=True, db_column='R', null=True)),
                ('c', models.FloatField(blank=True, db_column='C', null=True)),
                ('x', models.FloatField(blank=True, db_column='X', null=True)),
                ('u', models.FloatField(blank=True, db_column='U', null=True)),
                ('kingdom', models.TextField(blank=True, null=True)),
                ('phylum', models.TextField(blank=True, null=True)),
                ('taxClass', models.TextField(blank=True, db_column='class', null=True)),
                ('order', models.TextField(blank=True, null=True)),
                ('family', models.TextField(blank=True, null=True)),
                ('genus', models.TextField(blank=True, null=True)),
                ('species', models.TextField(blank=True, db_column='Species', null=True)),
                ('taxid', models.TextField(blank=True, db_column='Taxid', null=True)),
            ],
            options={
                'db_table': 'Props',
                'managed': False,
            },
        ),
    ]
