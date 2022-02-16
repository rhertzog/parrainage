# Installation locale

## Pré-requis

- Python 3.5.x (à tester avec des versions plus récentes)

## Installer

Créer un virtualenv :
```
python3.5 -m venv venv
source venv/bin/activate
```

Installer les dépendances Python :
```
pip install -r requirements.txt -r requirements-dev.txt
```


## Configurer la base de données

Par défaut, l’application utilisera une base de données SQLite (dans `parrainage/db.sqlite3`).

Pour créer les tables, il faut appliquer les migrations :
```
python manage.py migrate
```


## Charger les données

TODO


## Créer un super-utilisateur

```
python manage.py createsuperuser
```


## Lancer un serveur local

```
python manage.py runserver
```


## Lancer les tests

```
pytest
```
