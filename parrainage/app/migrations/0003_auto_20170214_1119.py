# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_elu_city_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='elu',
            name='city_address',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='elu',
            name='city_latitude',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='elu',
            name='city_longitude',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='elu',
            name='city_zipcode',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='elu',
            name='role',
            field=models.CharField(choices=[('M', 'Maire'), ('CD', 'Conseiller départemental'), ('CR', 'Conseiller régional'), ('D', 'Député'), ('S', 'Sénateur'), ('DE', 'Député européen')], max_length=2),
        ),
        migrations.AlterField(
            model_name='note',
            name='elu',
            field=models.ForeignKey(to='app.Elu', related_name='notes', on_delete=models.CASCADE),
        ),
        migrations.AlterField(
            model_name='note',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True, related_name='notes'),
        ),
    ]
