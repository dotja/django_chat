# Django chat app

A simple chat app in Django using channels.

```
## database migration
python manage.py makemigrations
python manage.py migrate


## start Redis container
docker run --name my-redis -p 6379:6379 -d redis

## run the app
python manage.py runserver
```
