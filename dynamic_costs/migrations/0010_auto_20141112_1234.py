# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import select2.fields


class Migration(migrations.Migration):

    dependencies = [
        ('entrances', '0011_auto_20141112_1214'),
        ('dynamic_costs', '0009_remove_dynamiccost_apartments'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApartmentDynamicCost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', models.DecimalField(null=True, verbose_name='Price', max_digits=8, decimal_places=2, blank=True)),
                ('is_paid', models.BooleanField(default=False, verbose_name='Is paid')),
                ('apartment', models.ForeignKey(to='entrances.Apartment')),
                ('cost', models.ForeignKey(to='dynamic_costs.DynamicCost')),
            ],
            options={
                'ordering': ('apartment__floor', 'apartment__apartment_integer'),
                'verbose_name': 'Apartment dynamic cost',
                'verbose_name_plural': 'Apartment dynamic costs',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='dynamiccost',
            name='apartments',
            field=select2.fields.ManyToManyField(to='entrances.Apartment', verbose_name='Apartments', through='dynamic_costs.ApartmentDynamicCost'),
            preserve_default=True,
        ),
    ]
