pip install locust


# Test Dev Setup
cd simple_app
docker-compose up -d --build
cd ..
locust -H http://127.0.0.1:8000 -f main.py --autostart -u 1000 -r 3 -t 600s RestApiTest
cd simple_app
docker-compose down -v


# Test Prod Setup
cd simple_app
docker-compose -f docker-compose.prod.yml up -d --build
cd ..
locust -H http://127.0.0.1:8000 -f main.py --autostart -u 1000 -r 3 -t 600s RestApiTest
cd simple_app
docker-compose -f docker-compose.prod.yml down -v
