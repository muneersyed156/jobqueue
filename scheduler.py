from flask import Flask,request
from celery import Celery
import json
import redis
from celery.result import AsyncResult
import task
app=Flask(__name__)

redis_host = "localhost"
redis_port = 6379
redis_password = ""
r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

@app.route("/insert",methods=["POST"])
def tasks():
    if(request.data):
        data=json.loads(request.data)
        return("Success")
    if(request.form):
        data=request.form
        # print(data["url"],data["time"])
        task_id=task.executing_task.delay(data["url"],data["time"])
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
