#!/bin/sh

if [ "$DATABASE" = "postgres" ]; then
    echo "Check if database is running.."

    while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
        sleep 0.1
    done

    echo "The database is up and running :-)"
fi

python src/manage.py migrate

python src/manage.py collectstatic --noinput

exec "$@"
