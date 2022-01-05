FROM python:alpine3.15
WORKDIR /code
COPY ./requirments.txt /code/requirments.txt
RUN pip install --no-cache-dir --upgrade -r requirments.txt  
COPY ./app /code/app

WORKDIR /code/app
EXPOSE 5001
# CMD uvicorn app:app --host $APP_HOST --port $APP_PORT 
# ENTRYPOINT [ " uvicorn " ," app:app "," --host "," $APP_HOST "," --port "," $APP_PORT " ]
 ENTRYPOINT ["uvicorn","app:app","--host","0.0.0.0","--port","5001"]
