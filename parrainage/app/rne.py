from datetime import datetime

from parrainage.app.models import Elu


def parse_elu(row):
    """
    Crée un élu à partir d'une ligne d’un fichier du Répertoire National des Élus

    https://www.data.gouv.fr/fr/datasets/repertoire-national-des-elus-1/
    """
    gender = "H" if row["Code sexe"] == "M" else "F"
    birthdate = datetime.strptime(row["Date de naissance"], "%d/%m/%Y").date()
    return Elu(
        first_name=row["Prénom de l'élu"],
        family_name=row["Nom de l'élu"],
        gender=gender,
        birthdate=birthdate,
        role="M",
        comment="Catégorie socio-professionnelle: {}".format(
            row["Libellé de la catégorie socio-professionnelle"]
        ),
        department=row["Code du département"],
        city=row["Libellé de la commune"],
        # city_size=int(row["Population"]),
        city_code=row["Code de la commune"],
        # nuance_politique=row["CodeNuancePolitique"],
    )


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
