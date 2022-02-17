import argparse
import csv
import logging

from django.core.management.base import BaseCommand
from django.db import transaction

from parrainage.app.models import Elu


DEPARTEMENTS = {
    "Ain": "01",
    "Aisne": "02",
    "Allier": "03",
    "Alpes-de-Haute-Provence": "04",
    "Hautes-Alpes": "05",
    "Alpes-Maritimes": "06",
    "Ardèche": "07",
    "Ardennes": "08",
    "Ariège": "09",
    "Aube": "10",
    "Aude": "11",
    "Aveyron": "12",
    "Bouches-du-Rhône": "13",
    "Calvados": "14",
    "Cantal": "15",
    "Charente": "16",
    "Charente-Maritime": "17",
    "Cher": "18",
    "Corrèze": "19",
    "Corse-du-sud": "2A",
    "Haute-corse": "2B",
    "Côte-d'Or": "21",
    "Côtes-d'Armor": "22",
    "Creuse": "23",
    "Dordogne": "24",
    "Doubs": "25",
    "Drôme": "26",
    "Eure": "27",
    "Eure-et-Loir": "28",
    "Finistère": "29",
    "Gard": "30",
    "Haute-Garonne": "31",
    "Gers": "32",
    "Gironde": "33",
    "Hérault": "34",
    "Ille-et-Vilaine": "35",
    "Indre": "36",
    "Indre-et-Loire": "37",
    "Isère": "38",
    "Jura": "39",
    "Landes": "40",
    "Loir-et-Cher": "41",
    "Loire": "42",
    "Haute-Loire": "43",
    "Loire-Atlantique": "44",
    "Loiret": "45",
    "Lot": "46",
    "Lot-et-Garonne": "47",
    "Lozère": "48",
    "Maine-et-Loire": "49",
    "Manche": "50",
    "Marne": "51",
    "Haute-Marne": "52",
    "Mayenne": "53",
    "Meurthe-et-Moselle": "54",
    "Meuse": "55",
    "Morbihan": "56",
    "Moselle": "57",
    "Nièvre": "58",
    "Nord": "59",
    "Oise": "60",
    "Orne": "61",
    "Pas-de-Calais": "62",
    "Puy-de-Dôme": "63",
    "Pyrénées-Atlantiques": "64",
    "Hautes-Pyrénées": "65",
    "Pyrénées-Orientales": "66",
    "Bas-Rhin": "67",
    "Haut-Rhin": "68",
    "Rhône": "69",
    "Haute-Saône": "70",
    "Saône-et-Loire": "71",
    "Sarthe": "72",
    "Savoie": "73",
    "Haute-Savoie": "74",
    "Paris": "75",
    "Seine-Maritime": "76",
    "Seine-et-Marne": "77",
    "Yvelines": "78",
    "Deux-Sèvres": "79",
    "Somme": "80",
    "Tarn": "81",
    "Tarn-et-Garonne": "82",
    "Var": "83",
    "Vaucluse": "84",
    "Vendée": "85",
    "Vienne": "86",
    "Haute-Vienne": "87",
    "Vosges": "88",
    "Yonne": "89",
    "Territoire de Belfort": "90",
    "Essonne": "91",
    "Hauts-de-Seine": "92",
    "Seine-Saint-Denis": "93",
    "Val-de-Marne": "94",
    "Val-d'Oise": "95",
    "Guadeloupe": "971",
    "Martinique": "972",
    "Guyane": "973",
    "La Réunion": "974",
    "Saint-Pierre-et-Miquelon": "975",
    "Mayotte": "976",
    "Saint-Barthélemy": "977",
    "Saint-Martin": "978",
}


class Command(BaseCommand):
    help = "Importer les parrainages validés par le Conseil constitutionnel"

    def add_arguments(self, parser):
        parser.add_argument(
            "fichier",
            help="fichier parrainagestotal.csv",
            type=argparse.FileType(mode="r", encoding="utf-8"),
        )
        parser.add_argument(
            "--candidate",
            help="nom et prénom de la candidate",
        )

    @transaction.atomic
    def handle(self, *args, **kwargs):
        nb_elus_mis_a_jour = 0
        reader = csv.DictReader(kwargs["fichier"], delimiter=";")
        for row in reader:
            try:
                elu = trouve_elu(row)
                if row["Candidat"] == kwargs["candidate"]:
                    if elu.status != Elu.STATUS_RECEIVED:
                        elu.status = Elu.STATUS_RECEIVED
                        elu.comment += f"\nParrainage publié par le CC le {row['Date de publication']}"
                        elu.save()
                        nb_elus_mis_a_jour += 1
                else:
                    if elu.status != Elu.STATUS_REFUSED:
                        elu.status = Elu.STATUS_REFUSED
                        elu.comment += f"\nParrainage donné à {row['Candidat']}, publié par le CC le {row['Date de publication']}"
                        elu.save()
                        nb_elus_mis_a_jour += 1
            except Elu.DoesNotExist:
                logging.warning(
                    "Pas trouvé de %s %s (%s de %s)",
                    row["Prénom"],
                    row["Nom"],
                    row["Mandat"],
                    (
                        row["Département"]
                        if row["Mandat"]
                        in ("Conseiller départemental", "Conseillère départementale")
                        else row["Circonscription"]
                    ),
                )
            except Elu.MultipleObjectsReturned:
                logging.error(
                    "Il y a plusieurs %s %s (%s de %s)",
                    row["Prénom"],
                    row["Nom"],
                    row["Mandat"],
                    (
                        row["Département"]
                        if row["Mandat"]
                        in ("Conseiller départemental", "Conseillère départementale")
                        else row["Circonscription"]
                    ),
                )
        print(f"Mis à jour le statut de {nb_elus_mis_a_jour} élus.")


def trouve_elu(row):
    filters = {
        "first_name": row["Prénom"],
        "family_name": row["Nom"],
    }
    # On essaie d’abord juste avec le nom, si ce n’est pas ambigu
    try:
        return Elu.objects.get(**filters)
    except Elu.DoesNotExist:
        # Sinon, des fois c’est la moitié d’un nom composé
        return Elu.objects.get(
            first_name=row["Prénom"],
            family_name__startswith=row["Nom"] + "-",
        )
    except Elu.MultipleObjectsReturned:
        # Sinon on essaie d’affiner avec le mandat indiqué par le CC
        if row["Mandat"] == "Maire":
            try:
                return Elu.objects.get(
                    role="M", city__iexact=row["Circonscription"], **filters
                )
            except Elu.DoesNotExist:
                # Sinon c’est un accent à enlever sur une capitale
                return Elu.objects.get(
                    role="M",
                    city__iexact=row["Circonscription"].replace("É", "E"),
                    first_name=row["Prénom"],
                    family_name=row["Nom"],
                )

        elif row["Mandat"] in (
            "Conseiller départemental",
            "Conseillère départementale",
        ):
            try:
                return Elu.objects.get(
                    role="CD", department=DEPARTEMENTS[row["Département"]], **filters
                )
            except Elu.DoesNotExist:
                # Il est peut-être aussi maire !
                return Elu.objects.get(
                    role="M",
                    department=DEPARTEMENTS[row["Département"]],
                    comment__contains="Autre mandat:",
                    **filters,
                )

        elif row["Mandat"] in (
            "Conseiller régional",
            "Conseillère régionale",
        ):
            try:
                return Elu.objects.get(role="CR", **filters)
            except Elu.DoesNotExist:
                # Il est peut-être aussi maire ou conseiller départemental
                return Elu.objects.get(
                    role__in=["M", "CD"],
                    department=DEPARTEMENTS[row["Département"]],
                    **filters,
                )

        elif row["Mandat"] in (
            "Sénateur",
            "Sénatrice",
        ):
            return Elu.objects.get(role="S", **filters)
        else:
            raise
