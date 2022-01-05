# from flask import Flask,request,json, Response
from fastapi import FastAPI ,HTTPException ,status
from pydantic.types import UUID4
import uvicorn
from MongoAPI import MongoAPI
from pydantic import BaseModel
from typing import Dict, Optional
import os


app = FastAPI(title = 'TEXT SEARCH API')
db =None
class Document(BaseModel):
    guid: UUID4
    title: str
    body: str
    data: dict
    fuzzy: Optional[str] = None

@app.get('/')
async def base():
    # return Response(response=js_dumps({"Status": "UP"}),
    #                 status=200,
    #                 mimetype='application/json')
    return {"Status": "UP"}

@app.get('/api/doc/read/{guid}')
async def mongo_read(guid:UUID4):
    response=db.read(guid)
    if response is None or response == []:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Document not found!")
    return response

@app.post('/api/doc/create')
async def mongo_create(document:Document,status_code=201):
    
    response,sucsess=db.create(document.dict())
    if not sucsess:
        #TODO ask if the same guid can be entered twice
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Document already exists")
    return response

@app.delete('/api/doc/delete/{guid}')
def mongo_delete(guid:UUID4):
    delete_cout=db.delete(guid)
    if delete_cout==0 :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Document not found!")
    return {'Status': 'Successfully Deleted'}

@app.get('/api/doc/search')
async def mongo_search():
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED,detail="not implemented")

def main():
    print("connected")
    global db
    data = {
        "database": "db",
        "collection": "photos",
    }
    db=MongoAPI(data)
# main()
if __name__ == '__main__':
    #TODO GET FROM ENVIROMENT VARIABLE
    data = {
        "database": "db",
        "collection": "photos",
    }

    # db=MongoAPI(data)

    uvicorn.run('app:app',debug=True, reload=True,port=os.environ['APP_PORT'], host=os.environ['APP_HOST'])