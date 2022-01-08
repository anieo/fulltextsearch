FROM python:alpine3.15
WORKDIR /code
COPY ./requirments.txt /code/requirments.txt
RUN apk add gcc libc-dev
RUN pip install --no-cache-dir --upgrade -r requirments.txt  
COPY ./app /code/app

WORKDIR /code/app
EXPOSE $APP_PORT
CMD uvicorn app:app --host $APP_HOST --port $APP_PORT 
# # ENTRYPOINT [ " uvicorn " ," app:app "," --host "," $APP_HOST "," --port "," $APP_PORT " ]
# ENTRYPOINT ["uvicorn","app:app","--host",$APP_HOST,"--port",$APP_PORT]
