from celery import Celery
import time
import redis
import json
import requests
import pymongo
#celery -A task worker --pool=solo --loglevel=info
celery=Celery('task',backend='redis://localhost/0',broken='redis://localhost/0')

obj=pymongo.MongoClient()
db=obj.scheduler

@celery.task()
def executing_task(url,ide=0,delay=0):
    delay=int(delay)
    #db.scheduler.update_one({"id":ide},{"$set":{"status":'WAITING'}})
    time.sleep(delay//1000)
    #db.scheduler.update_one({"id":ide},{"$set":{"status":'RUNNING'}})
    try:
        result=requests.get(url)
        if(result.status_code==200):
        #    db.scheduler.update_one({"id":ide},{"$set":{"status":'SUCCESS'}})
            print(result.text)
            return(str(result.text))
        else:
        #    db.scheduler.update_one({"id":ide},{"$set":{"status":'FAILED'}})
            return("FAILED")
    except Exception as e:
        #db.scheduler.update_one({"id":ide},{"$set":{"status":'FAILURE'}})
        return(e)

