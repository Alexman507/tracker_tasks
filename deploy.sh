#python3 -m venv env
#source env/bin/activate
#pip3 install -r requirements.txt
#python3 manage.py migrate
#python3 manage.py collectstatic --no-input
#deactivate
docker-compose up --build -d
docker-compose exec app python manage.py migrate

#Если нужно создать суперпользователя (настройки переназначить можно в users/management/commands/csu.py)
#docker-compose exec app python manage.py csu