from __future__ import annotations
from functools import wraps
from typing import Any
import redis

from fastapi import HTTPException, status
from sqlalchemy import delete, func, insert, select, update
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .base import DB, inject_db
from .models import Topics
from SNS import schemas
from sqlalchemy.orm import scoped_session
from typing import Any, Callable, TypeVar


r  = redis.Redis(host='localhost', port=6379, db=0)


Fn = TypeVar("Fn", bound=Callable[..., Any])

def check_db_connected(fn: Fn) -> Any:
    @wraps(fn)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        await inject_db()
        db = DB.get()
        assert db is not None, "Database is not connected."
        return await fn(*args, **kwargs)
    return wrapper

@check_db_connected
async def create_topic(topicc) -> Any:
    db = DB.get()
    async with db.transaction():
        query = insert(Topics)
        await db.execute(query,{"set_name": topicc.set_name, "topic_name": topicc.topic_name, "creator_user_id": topicc.creator_user_id, "access_policy": topicc.access_policy})
    return None




async def get_topic_info(topic_name) -> Any:

    cached_data = r.get(topic_name)

    if cached_data:
        print("Veri Redis cache'te bulundu")
        new = cached_data.decode('utf-8')
        yusuf = []
        yusuf.append(new)
        return yusuf
    else:
        # Veri Redis cache'te bulunamadı, başka bir kaynaktan alınması gerekiyor
        data = await fetch_data_from_source(topic_name)
        print("2")
        print(type(data[0]))
        print(data)
        print(data[0])
        x = data[0]
        y = str(x)
        print(type(y))
        # Veriyi Redis cache'e kaydetme

        r.set(topic_name, y)

        print("3")
        return data


@check_db_connected
async def fetch_data_from_source(topic_name):

    print("Retrieving data from MySQL...")
    query = select([Topics]).where(Topics.c.topic_name == topic_name)
    db = DB.get()
    topic_info = []
    result = await db.fetch_one(query)
    topic_info.append(result)
    if result == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Topic Not found for topic name : {}".format(topic_name),
        )
    else:
        return topic_info
    
    