#!/bin/bash
# export $(cat app.env | xargs )
# docker build -t text-search-api .
# docker network create text-app
# docker rm -f mongo text-search mongodb
# export MONGO_DB=db MONGO_PORT=5000 MONGO_USER=MONGO MONGO_PASSWORD=MONGO

# # docker run -d --name mongodb  -p $5000:27017 --rm -e MONGO_USER="$MONGO_USER" -e MONGO_PASSWORD="$MONGO_PASSWORD" -e MONGO_DB="$MONGO_DB" mongo
# # export MONGO_HOST=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' mongodb)
# # echo $MONGO_HOST
# docker run -d -v $DAT_VOLUME:/data/db --name $DAT_CONTAINER -p $DAT_PORT:27017 \
#     -e MONGO_INITDB_ROOT_USERNAME=$DB_USER \
#     -e MONGO_INITDB_ROOT_PASSWORD=$DB_PASSWORD \
#     -e MONGO_INITDB_DATABASE=db
#     mongo

# docker run  --name text-search --env-file  ./app.env -e MONGO_HOST=$MONGO_HOST   -p $APP_PORT:$APP_PORT \
#     text-search-api

docker-compose --env-file app.env up
