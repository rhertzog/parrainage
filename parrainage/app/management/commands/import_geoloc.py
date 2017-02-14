# Copyright 2017 Raphaël Hertzog
#
# This file is subject to the license terms in the LICENSE file found in
# the top-level directory of this distribution.

import argparse
from datetime import datetime
import csv
import logging
import sys

from django.core.management.base import BaseCommand
from django.db import transaction

from parrainage.app.models import Elu

class Command(BaseCommand):
    help = 'Import a CSV file with data about mayors'

    def add_arguments(self, parser):
        parser.add_argument('csvfile', help='Path of the CSV file',
                            type=argparse.FileType(mode='r', encoding='utf-8'))

    @transaction.atomic
    def handle(self, *args, **kwargs):
        csvfile = csv.DictReader(kwargs['csvfile'], delimiter=';',
                                 restkey='addresses')

        for row in csvfile:
            done = False
            for elu in Elu.objects.filter(city_code=row['city_code']):
                elu.city_address = '\n'.join(row.get('addresses', [])) or ''
                elu.city_zipcode = row['city_zipcode'] or ''
                elu.city_latitude = row['latitude'] or ''
                elu.city_longitude = row['longitude'] or ''
                elu.save()
                done = True
            if not done:
                sys.stderr.write(
                    'Unknown city code: {}\n'.format(row['city_code']))
