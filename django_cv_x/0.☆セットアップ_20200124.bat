@echo off
echo https://ta7uw.hatenablog.com/entry/2018/01/19/160517

pip install --upgrade Django
pip install --upgrade djangorestframework
pip install --upgrade chainer
pip install --upgrade chainerCV

pause

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

pause

python manage.py runserver

pause

echo http://127.0.0.1:8000/admin

curl -X POST http://localhost:8000/item/detection/ -F "image=@cat.jpeg" | jq
curl -X POST http://localhost:8000/item/detection/ -F "image=@dog_cat.jpg" | jq

pause



