# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import select2.fields


class Migration(migrations.Migration):

    dependencies = [
        ('entrances', '0021_apartmentdocument'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='apartmentdocument',
            options={'verbose_name': 'Uploaded document', 'verbose_name_plural': 'Uploaded documents'},
        ),
        migrations.AlterModelOptions(
            name='entrance',
            options={'verbose_name': 'Entrance', 'verbose_name_plural': 'Entrances'},
        ),
        migrations.AlterModelOptions(
            name='entrancedocument',
            options={'verbose_name': 'Uploaded document', 'verbose_name_plural': 'Uploaded documents'},
        ),
        migrations.AlterField(
            model_name='apartment',
            name='contact_email',
            field=models.CharField(max_length=255, null=True, verbose_name='Contact email', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='apartment',
            name='contact_person',
            field=models.CharField(max_length=255, null=True, verbose_name='Contact person', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='apartment',
            name='contact_phone',
            field=models.CharField(max_length=255, null=True, verbose_name='Contact phone', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='apartment',
            name='entrance',
            field=select2.fields.ForeignKey(verbose_name='Entrance', to='entrances.Entrance'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entrancedocument',
            name='document',
            field=models.FileField(upload_to=b'entrancedocuments/%Y/%m', verbose_name='Document'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entrancedocument',
            name='entrance',
            field=models.ForeignKey(verbose_name='Entrance', to='entrances.Entrance'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='monthlyexpence',
            name='entrance',
            field=models.ForeignKey(verbose_name='Entrance', to='entrances.Entrance'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='monthlyexpence',
            name='task_type',
            field=models.ForeignKey(verbose_name='Task type', to='nomenclatures.TaskType'),
            preserve_default=True,
        ),
    ]
