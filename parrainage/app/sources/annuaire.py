import csv

from parrainage.app.models import Elu


def read_csv(iterable):
    return csv.DictReader(iterable, delimiter=",")


def met_a_jour_coordonnees_elus(row_annuaire):
    for elu in Elu.objects.filter(city_code=row_annuaire["codeInsee"]):
        elu.public_email = row_annuaire["Email"]
        elu.public_phone = row_annuaire["Téléphone"]
        elu.public_website = row_annuaire["Url"]
        elu.city_address = row_annuaire["Adresse"]
        elu.city_zipcode = row_annuaire["CodePostal"]
        elu.city_latitude = row_annuaire["Latitude"]
        elu.city_longitude = row_annuaire["Longitude"]
        elu.save()
