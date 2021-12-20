# Final Year Project

## Abstract Styler

### To Build the Project

* docker-compose up -d --build (Dev build)
* docker-compose -f docker-compose.prod.yml up -d --build (Production build)
* Access at http://localhost:5000

### To destroy project and volumes

* docker-compose down -v

### To Inspect DB

* docker-compose exec db psql --username=root --dbname=finalyear
    * \c finalyear
    * [Insert SQL commands]
    * \q to exit



