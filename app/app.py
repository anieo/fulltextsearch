from fastapi import FastAPI ,HTTPException ,status
from nltk.sem.evaluate import Error
from pydantic.types import UUID4
from starlette.responses import Response
import uvicorn
from MongoAPI import MongoAPI
from pymongo import errors
from pydantic import BaseModel
from typing import Dict, Optional
import os
import fuzzy
import nltk
from nltk.corpus import stopwords
from nltk import word_tokenize
import re
data = {
    "database": "db",
    "collection": "photos",
    }
try:
    db =MongoAPI(data)
except errors.AutoReconnect as error:
    print("Conniction to Database failed")
    print("Message : ",error._message)
    raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,detail="Database Unavilable ")
except errors.PyMongoError as error:
    print("Message")
    raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,detail="Database Unavilable ")

nltk.download('punkt')
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

app = FastAPI(title = 'TEXT SEARCH API')
class Document(BaseModel):
    guid: UUID4
    title: str
    body: str
    data: dict
    fuzzy: Optional[str] = None
class SearchQuery(BaseModel):
    query: str
    limit: Optional[int]=10
    threshold: Optional[float]=0.6
    fuzzy: Optional[bool]=True
    
@app.get('/')
async def base():
    # return Response(response=js_dumps({"Status": "UP"}),
    #                 status=200,
    #                 mimetype='application/json')
    return {"Status": "UP"}

@app.get('/api/doc/read/{guid}')
async def mongo_read(guid:UUID4):
    try:
        response=db.read(guid)
    except errors.PyMongoError as error:
        print(error._message)
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,detail="Connection error")

    if response is None or response == []:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Document not found!")
    return response

@app.post('/api/doc/create')
async def mongo_create(document:Document,status_code=201):
    document.fuzzy=fill_fuzzy(document.title,document.body)
    try:
        guid,sucsess=db.create(document.dict())
    except errors.WriteError as error:
        print(error._message)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Write error")
        
    if not sucsess:
        #TODO ask if the same guid can be entered twice
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Document already exists")
    response = {'Status': 'Successfully Inserted',
                  'guid': guid}
    return response

def clear(words):
    words = re.sub(r'\d+', '', words)
    words= word_tokenize(words)
    words= [word for word in words if word.isalnum() and word.lower() not in stop_words]
    return words
def fuzzy_text(text):
    f=""
    for word in text:
        f=f+" "+ fuzzy.nysiis(word)
    return f
def fill_fuzzy(title,body):
    
    body = clear(body)
    title = clear(title)
    f=fuzzy_text(title)+fuzzy_text(body)
    return f

@app.delete('/api/doc/delete/{guid}')
def mongo_delete(guid:UUID4):
    try:
        delete_cout=db.delete(guid)
        if delete_cout==0 :
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Document not found!")
        return {'deleted': guid}
    except errors.WriteError as error:
        print(error._message)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Document already exists")
    except errors.PyMongoError as error:
        print(error._message)
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,detail="Connection error")

        

@app.get('/api/doc/search')
async def mongo_search(q:SearchQuery):
    search_text=""
    if q.fuzzy:
        search_text=fuzzy_text(clear(q.query))
    else:
        for i in clear(q.query):
            
            search_text=search_text+"(?=.*"+i+")"
        # print(search_text)    
        # search_text=q.query
    try:
        res=db.search(search_text,q.fuzzy,q.limit,q.threshold)
    except errors.PyMongoError as error:
        print(error._message)
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,detail="Connection error")

    # print(a)
    print(res)
    
    return res


if __name__ == '__main__':

    uvicorn.run('app:app',debug=True, reload=True,port=os.environ['APP_PORT'], host=os.environ['APP_HOST'])