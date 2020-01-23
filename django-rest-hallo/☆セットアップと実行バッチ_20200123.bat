@echo off
echo https://github.com/argenisosorio/django-rest-framework-example

echo $ pip install -r requirements.txt
pip install --upgrade Django
pip install --upgrade djangorestframework

pause

python manage.py migrate
python manage.py createsuperuser
python manage.py migrate
python manage.py runserver

pause

echo http://127.0.0.1:8000/admin
echo See results in:
echo http://127.0.0.1:8000/users
echo http://127.0.0.1:8000/groups

pause



