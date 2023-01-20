import random
import logging
import datetime
from asyncio import run
from mongo import MongoDB
from fastapi import FastAPI
from pymongo import MongoClient
from datetime import date, timedelta
from request_form import LabeledData, CheckedData
from fastapi.middleware.cors import CORSMiddleware


## Static Parameters
DATA_LENGTH = 72706

## Connections
mongo = MongoDB()
app = FastAPI()
logger = logging.getLogger()

## Middleware (for testing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

## APIs
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/api/count/visit")
async def visit_count():
    
    today = date.today()
    out = await mongo.find_one("hate_data", "view_count", {"date": str(today)})
    if out == None:
        out = await mongo.insert_one("hate_data", "view_count", {"date": str(today), "count": 1})
    else:
        out = await mongo.update_one("hate_data", "view_count", {"date": str(today)}, {"count": out["count"] + 1})
    
    return {"result": "ok"}


@app.get("/api/get_text")
async def get_text():
    ## Get random data which status is not 0
    while True:
        id = random.randrange(0, DATA_LENGTH)
        info = {"_id": id}
        
        data = await mongo.find_one("hate_data", "hate_data", info)
        if not data["status"]:
            break
        
    text = data["text"]
    return {"text": text, "text_id": id}


@app.put("/api/labeling")
async def labeling(request : LabeledData):
    ## Get request
    if request.check1:
        check_box = 1
    elif request.check2:
        check_box = 2
    else:
        check_box = 3
        
    id = request.id
    text = request.text
    target = request.labeledText
    nick_name = request.nickName
    
    ## Update the hate data
    info = {"_id": id}
    data = await mongo.update_one("hate_data", "hate_data", info, {"status": 1})
    
    ## Store to need check collection
    info = {
        "_id": id,
        "text": text,
        "target": target,
        "label": check_box,
        "nick_name": nick_name
    }
    data = await mongo.insert_one("hate_data", "need_check_data", info)
    
    ## Labeled count
    today = date.today()
    out = await mongo.find_one("hate_data", "labeled_count", {"date": str(today)})
    if out == None:
        out = await mongo.insert_one("hate_data", "labeled_count", {"date": str(today), "count": 1})
    else:
        out = await mongo.update_one("hate_data", "labeled_count", {"date": str(today)}, {"count": out["count"] + 1})
        
    ## Get random data which status is not 0
    while True:
        id = random.randrange(0, DATA_LENGTH)
        info = {"_id": id}
        
        data = await mongo.find_one("hate_data", "hate_data", info)
        if not data["status"]:
            break
        
    text = data["text"]
    return {"text": text, "text_id": id}


@app.get("/api/get_need_check")
async def get_need_check():
    out = await mongo.find_many("hate_data", "need_check_data", data={}, limit=20)
    
    response = {}
    for i in range(len(out)):
        response["data"+str(i)] = out[i]
    
    return response


@app.post("/api/permit")
async def permit(request: CheckedData):
    id = request.id
    text = request.text
    target = request.target
    nick_name = request.nick_name
    label = request.label
    
    ## 1. delete data in need_check
    out = await mongo.delete_one("hate_data", "need_check_data", {"_id": id})
    
    ## 2. update in hate data -> 2 + update target
    if label == 1:
        status = 3
    elif label == 2:
        status = 4
    else:
        status = 2
    print(status)
    out = await mongo.update_one("hate_data", "hate_data", {"_id": id}, {"target": target, "status": status})
    
    ## 3. user info update
    out = await mongo.find_one("hate_data", "user_info", {"nick_name": nick_name})
    if out == None:
        out = await mongo.insert_one("hate_data", "user_info", {"nick_name": nick_name, "count": 1})
    else:
        out = await mongo.update_one("hate_data", "user_info", {"nick_name": nick_name}, {"count": out["count"] + 1})
    
    ## 4. labeled count by date
    today = date.today()
    out = await mongo.find_one("hate_data", "target_count", {"date": str(today)})
    if out == None:
        out = await mongo.insert_one("hate_data", "target_count", {"date": str(today), "count": 1})
    else:
        out = await mongo.update_one("hate_data", "target_count", {"date": str(today)}, {"count": out["count"] + 1})
    print("ok")
    
    return {"result": "ok"}


@app.post("/api/reject")
async def reject(request: CheckedData):
    id = request.id
    text = request.text
    target = request.target
    nick_name = request.nick_name
    
    ## 1. delete data in need_check
    out = await mongo.delete_one("hate_data", "need_check_data", {"_id": id})
    ## 2. update in hate data -> 0 original
    out = await mongo.update_one("hate_data", "hate_data", {"_id": id}, {"target": target, "status": 0})
    print("reject")
    
    return {"result": "reject"}


@app.get("/api/count/get_top_user")
async def get_top_user():
    ## 1. get user infomation
    out = await mongo.find_many("hate_data", "user_info", {}, "count", 10)
    out = list(out)
    out = out[-10:]
    
    response = []
    for item in out:
        response.append({"x": item["nick_name"], "y": item["count"]})
        
    return {"data": response}



@app.get("/api/count/daily_labeled")
async def daily_labeled():
    return

@app.get("/api/count/daily_permited")
async def daily_permited():
    return

