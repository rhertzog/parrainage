# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models, transaction
import django.utils.crypto

@transaction.atomic
def add_private_tokens(apps, schema_editor):
    Elu = apps.get_model('app', 'Elu')
    for elu in Elu.objects.filter(private_token__isnull=True):
        elu.private_token = str(django.utils.crypto.get_random_string())
        elu.save()


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20170225_0940'),
    ]

    operations = [
        migrations.AddField(
            model_name='elu',
            name='private_token',
            field=models.CharField(max_length=20, editable=False, default=None, null=True),
        ),
        migrations.RunPython(add_private_tokens),
        migrations.AlterField(
            model_name='elu',
            name='private_token',
            field=models.CharField(editable=False, max_length=20, default=django.utils.crypto.get_random_string),
        ),
    ]
