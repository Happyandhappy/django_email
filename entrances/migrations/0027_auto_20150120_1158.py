# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entrances', '0026_monthlyexpence_assignee'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentsCashier',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'verbose_name': 'Payments cashier',
                'verbose_name_plural': 'Payments cashier',
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='entrance',
            options={'ordering': ('title',), 'verbose_name': 'Entrance', 'verbose_name_plural': 'Entrances'},
        ),
        migrations.AlterField(
            model_name='apartment',
            name='monthly_fee',
            field=models.DecimalField(null=True, verbose_name='Monthly fee', max_digits=8, decimal_places=2, blank=True),
            preserve_default=True,
        ),
    ]
