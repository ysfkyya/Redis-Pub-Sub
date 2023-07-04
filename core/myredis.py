import redis
from SNS import core
from SNS.schemas import topic
from SNS.api import topic
import json
from fastapi import FastAPI, HTTPException



r = redis.Redis(host='localhost', port=6379, db=0)


async def create_topic(topicc) -> None:
    
    topic_data = {
        "display_name": topicc.topic_name,
        "creator_user_id": topicc.creator_user_id,
        "access_policy": topicc.access_policy
    }

    print("create2")
    r.sadd(topicc.set_name, json.dumps(topic_data))

    print ({"message": f'Topic "{topicc.topic_name}" created successfully.'})


async def list_topic(set_name) -> None:

    topic_list = []
    for topic_data in r.smembers(set_name):
        topic = json.loads(topic_data)
        topic_list.append(topic)
        print(topic)
    return topic_list
    
async def delete_topic(set_name, topic_name) -> None:

    if not r.exists(set_name):
        raise HTTPException(status_code=404, detail=f"Set '{set_name}' not found")
    
    for topic_data in r.smembers(set_name):
        topic = json.loads(topic_data)
        if topic["display_name"] == topic_name:
            r.srem(set_name, topic_data)
            return {"message": f"Topic '{topic_name}' deleted from set '{set_name}'"}
    
    raise HTTPException(status_code=404, detail=f"Topic '{topic_name}' not found in set '{set_name}'")

