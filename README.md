# Outil de suivi des parrainages

## Sources de données

- [Répertoire national des élus](https://www.data.gouv.fr/fr/datasets/repertoire-national-des-elus-1/)
- [Annuaire de l’administration](https://www.data.gouv.fr/fr/datasets/service-public-fr-annuaire-de-l-administration-base-de-donnees-locales/)


## Installation locale

### Pré-requis

- Python 3.7.x


### Installer

Créer un virtualenv :
```
python3.7 -m venv venv
source venv/bin/activate
```

Installer les dépendances Python :
```
pip install -r requirements.txt -r requirements-dev.txt
```


### Configurer la base de données

Par défaut, l’application utilisera une base de données SQLite (dans `parrainage/db.sqlite3`).

Pour créer les tables, il faut appliquer les migrations :
```
python manage.py migrate
```


### Charger les données

#### Liste des maires

- Récupérer `rne-maires.csv` depuis https://www.data.gouv.fr/fr/datasets/repertoire-national-des-elus-1/

- Récupérer `mairies.csv` depuis https://www.data.gouv.fr/fr/datasets/service-public-fr-annuaire-de-l-administration-base-de-donnees-locales/

- Lancer la commande (ça peut être long...) :
```
python manage.py import_maires rne-maires.csv mairies.csv
```

#### Liste des conseillers départementaux

- Récupérer `rne-cd.csv` depuis https://www.data.gouv.fr/fr/datasets/repertoire-national-des-elus-1/

- Lancer la commande (ça peut être long...) :
```
python manage.py import_elus --mandat=CD rne-cd.csv
```

#### Liste des conseillers régionaux

- Récupérer `rne-cr.csv` depuis https://www.data.gouv.fr/fr/datasets/repertoire-national-des-elus-1/

- Lancer la commande :
```
python manage.py import_elus --mandat=CR rne-cr.csv
```

#### Liste des sénateurs

- Récupérer `rne-sen.csv` depuis https://www.data.gouv.fr/fr/datasets/repertoire-national-des-elus-1/

- Lancer la commande :
```
python manage.py import_elus --mandat=S rne-sen.csv
```


### Créer un super-utilisateur

```
python manage.py createsuperuser
```


### Lancer un serveur local

```
python manage.py runserver
```


### Lancer les tests

```
pytest
```

ou, pour les lancer en continu :

```
ptw
```
