web: gunicorn parrainage.project.wsgi --log-file -
postdeploy: python manage.py migrate && python manage.py create_initial_admin_user
