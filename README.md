# Final Year Project

## Abstract Styler

### To Build the Project

* docker-compose -f docker-compose.yml up -d --build (Dev build)
* Access at http://localhost:5000 (Dev build)

* docker-compose -f docker-compose.prod.yml up -d --build (Production build)
* docker-compose -f docker-compose.prod.yml exec web python manage.py create_db (Create DB tables (First time only))
    * Access frontend at http://localhost:9000 (Production NGinx reverse proxy)
    * Access backend at http://localhost:9000/api (Production NGinx reverse proxy)

### To destroy project and volumes

* docker-compose -f docker-compose.yml down -v (Dev build)
* docker-compose -f docker-compose.prod.yml down -v (Production build)

### To Inspect DB

* docker-compose exec db psql --username=root --dbname=finalyear
    * \c finalyear
    * [Insert SQL commands]
    * \q to exit



