from celery import Celery
import time
import redis
import json
import requests
#celery -A task worker --pool=solo --loglevel=info
celery=Celery('task',backend='redis://localhost/0',broken='redis://localhost/0')


@celery.task()
def executing_task(url,delay=0):
    delay=int(delay)
    time.sleep(delay//1000)
    result=requests.get(url)
    return(str(result))

