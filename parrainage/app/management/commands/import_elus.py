# Copyright 2017 Raphaël Hertzog
#
# This file is subject to the license terms in the LICENSE file found in
# the top-level directory of this distribution.

import argparse
from datetime import datetime
import csv
import logging

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
        csvfile = csv.DictReader(kwargs['csvfile'])
        elus = []
        civilite_mapping = {
            'M': 'H',
            'F': 'F',
            'H': 'H',
            'M.': 'H',
            'Mme': 'F',
            'Mlle': 'F',
        }
        for row in csvfile:
            gender = civilite_mapping.get(row['Civilité'], '')
            birthdate = datetime.strptime(row['DateNaissance'],
                                          '%Y-%m-%d').date()
            try:
                elu = Elu.objects.get(
                    first_name=row['PrénomÉlu'],
                    family_name=row['NomÉlu'],
                    birthdate=birthdate,
                )
                if elu.role == row['Role']:
                    continue
                if row['Role'] == 'CD':
                    comment = 'Autre mandat: Conseiller départemental'
                elif row['Role'] == 'CR':
                    comment = 'Autre mandat: Conseiller régional'
                elif row['Role'] == 'S':
                    comment = 'Autre mandat: Sénateur'
                elu.comment = '{}\n{}'.format(comment, elu.comment)
                elu.save()
            except Elu.DoesNotExist:
                elu = Elu(
                    first_name=row['PrénomÉlu'],
                    family_name=row['NomÉlu'],
                    gender=gender,
                    birthdate=birthdate,
                    role=row['Role'],
                    department=row['CodeDépartement'],
                    nuance_politique=row['CodeNuancePolitique'],
                )
                elus.append(elu)
            except Elu.MultipleObjectsReturned:
                logging.error('Multiple {} {} born on {}'.format(
                    row['PrénomÉlu'], row['NomÉlu'], birthdate))
        Elu.objects.bulk_create(elus)
