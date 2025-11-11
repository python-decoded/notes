# run service locally
cd services/web
export FLASK_APP=project/__init__.py
python manage.py run


# docker 
docker-compose build
docker-compose up -d
docker-compose up -d --build

docker-compose stop
docker-compose down -v

# specify docker-compose
docker-compose -f docker-compose.yml [COMMAND]


# create db
docker-compose exec web python manage.py create_db
docker-compose exec web python manage.py seed_db

# check volume
docker volume inspect flask-on-docker_postgres_data

# check error logs
docker-compose logs -f
docker-compose logs -f web
docker-compose logs -f db

# connect to db
docker-compose exec db psql --username=hello_flask --dbname=hello_flask_dev


# run single web service
docker build -f ./services/web/Dockerfile -t hello_flask:latest ./services/web
docker run \
    -p 5001:5000 \
    -e "FLASK_APP=project/__init__.py" \
    -e "FLASK_ENV=development" \
    hello_flask python /usr/src/app/manage.py run -h 0.0.0.0
