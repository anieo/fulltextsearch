import requests as r
import json
import os

url="http://localhost:5001/api/doc"
def Create(file):
    response = r.post(url=url+"/create",json=file)
    print("Create :\t",url+"/create",response.status_code)
    return json.loads(response.content)['guid']
def Delete(guid):
    response = r.delete(url=url+"/delete/"+guid)
    print("Delete :\t",url+"/delete/"+guid,response.status_code)
    return json.loads(response.content)['deleted']

def Read(guid):
    response = r.get(url=url+'/read/'+guid)
    print("Read : \t",url+"/read/"+guid,response.status_code)
    return json.loads(response.content)
class search_request:
	query:str
	limit:int
	fuzzy:bool
	threshold:float

def Search(query,fuzzy,limit,threshold):
    sr=search_request()
    sr.query=query
    sr.fuzzy=fuzzy
    sr.limit=limit
    sr.threshold=threshold
    js=sr.__dict__
    print(js)
    response = r.get(url=url+'/search',json=js)
    print("Search : \t",url+"/search",response.status_code)
    return json.loads(response.content)

json_files="jsonDocuments"
paths=[]
files=[]
for i in os.listdir(json_files):
    full_path = os.path.join(json_files,i)
    print(full_path)
    if os.path.isfile(full_path):
        paths.append(full_path)
print(paths)
for i in paths:
    print("File : ",i.split('/')[-1])
    #create
    with  open(i,'r') as f:
        files.append(json.loads(f.read()))
    print()
    guid=Create(files[-1])
    print("Created : ",guid)
    #read
    nguid=Read(guid)
    print("Read : ",nguid)
print("Finished loading data")
while True:
    print("Enter 1: Search")
    print("Enter 2: Delete")
    print("Enter 3: Read")
    print("Enter 4: Create")
    print("Enter 5: Exit")
    c=int(input("Select: "))
    if c==1 :
        query=input("Query :\t")
        fuzzy=int(input("Fuzzy (EX :1 or 0):\t"))
        limit=int(input("Limit (EX : 10) = \t"))
        threshold=float(input("Threshold (EX : 0.6) = \t"))
        fuzzy=fuzzy == 1
        res=Search(query,fuzzy,limit,threshold)
        print("***************","Search Results","***************")
        print(json.dumps(res,indent=4))
        print("***************","**************","***************")
        pass
    elif c==2 :
        i=int(input("Enter file no :\t"))
        rguid=Delete(files[i]['guid'])
        print("Deleted ",rguid)
        print("***************","**************","***************")
        pass
    elif c==3 :
        i=int(input("Enter Guid :\t"))
        res=Read(files[i]['guid'])
        print("****************","Read Results","****************")
        print(json.dumps(res,indent=4))
        print("****************","************","****************")
        pass
    elif c==4 :
        i=int(input("Enter file number:\t"))
        res=Create(files[i])
        pass
    elif c==5:
        print("Exit")
        print("********************","Exit","********************")

        break

    
    

