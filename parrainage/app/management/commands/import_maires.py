# Copyright 2017 Raphaël Hertzog
#
# This file is subject to the license terms in the LICENSE file found in
# the top-level directory of this distribution.

import argparse
from datetime import datetime
import csv
import logging

from django.core.management.base import BaseCommand

from parrainage.app.models import Elu

class Command(BaseCommand):
    help = 'Import a CSV file with data about mayors'

    def add_arguments(self, parser):
        parser.add_argument('csvfile', help='Path of the CSV file',
                            type=argparse.FileType(mode='r', encoding='utf-8'))

    def handle(self, *args, **kwargs):
        csvfile = csv.DictReader(kwargs['csvfile'])
        elus = []
        for row in csvfile:
            gender = 'H' if row['Civilité'] == 'M' else 'F'
            birthdate = datetime.strptime(row['DateNaissance'],
                                          '%Y-%m-%d').date()
            elu = Elu(
                first_name=row['PrénomMaire'],
                family_name=row['NomMaire'],
                gender=gender,
                birthdate=birthdate,
                role='M',
                comment='Catégorie socio-professionnelle: {}'.format(
                    row['CatégorieSocioProfessionelle']),
                public_email=row['EmailMairie'],
                public_phone=row['TelMairie'],
                public_website=row['UrlMairie'],
                department=row['CodeDépartement'],
                city=row['Commune'],
                city_size=int(row['Population']),
                city_code=row['codeinsee'],
                nuance_politique=row['CodeNuancePolitique'],
            )
            elus.append(elu)
        Elu.objects.bulk_create(elus)
