# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import select2.fields


class Migration(migrations.Migration):

    dependencies = [
        ('nomenclatures', '0012_remove_tasktype_from_cash_desk'),
        ('entrances', '0014_apartment_monthly_fee'),
    ]

    operations = [
        migrations.CreateModel(
            name='MonthlyExpence',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', models.DecimalField(null=True, verbose_name='Price', max_digits=8, decimal_places=2, blank=True)),
                ('apartment', models.ForeignKey(verbose_name='Apartment', to='entrances.Apartment')),
                ('task_type', models.ForeignKey(verbose_name='task type', to='nomenclatures.TaskType')),
            ],
            options={
                'verbose_name': 'Monthly expence',
                'verbose_name_plural': 'Monthly expences',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='apartment',
            name='monthly_expences',
            field=select2.fields.ManyToManyField(to='nomenclatures.TaskType', verbose_name='Monthly expences', through='entrances.MonthlyExpence'),
            preserve_default=True,
        ),
    ]
