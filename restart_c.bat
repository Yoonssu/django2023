@echo "-----makemigrations--------"
python manage.py makemigrations
@echo "-----migrations--------"
python manage.py migrate
@echo "-----runserver--------"
python manage.py runserver