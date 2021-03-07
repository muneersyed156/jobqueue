from flask import Flask,request
from celery import Celery
import json
import redis
from celery.result import AsyncResult
import task
import pymongo
app=Flask(__name__)

redis_host = "localhost"
redis_port = 6379
redis_password = ""
r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

obj=pymongo.MongoClient()
db=obj.scheduler

@app.route("/insert",methods=["POST"])
def tasks():
    if(request.data):
        data=json.loads(request.data)
        return("Success")
    if(request.form):
        data=request.form
        k=db.scheduler.count()
        print("Entered calling async")
        task_id=task.executing_task.delay(data["url"],k+1,data["time"])
        print("Exiting calling async")
        db.scheduler.insert_one({"id":k+1,"url":data["url"],"waittime":data["time"],'scheduled_id':task_id.id,'status':'SCHEDULED'})
        return(task_id.id)
        
@app.route("/<taskId>",methods=["GET"])
def get_task_status(taskId):
    if(taskId!=''):
        keys=r.keys()
        task_name='celery-task-meta-'+taskId
        if( task_name in keys):
            data=json.loads(r.get(task_name))
            return(json.dumps(data))
        else:
            return

if __name__=="__main__":
    app.run(debug=True,port=8081,threaded=True)
