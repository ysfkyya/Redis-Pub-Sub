from fastapi import APIRouter, Header, Request, HTTPException, status, FastAPI
from SNS.schemas import common
from SNS.schemas import topic
from SNS.core import myredis
from typing import List
import json
from SNS.db import api as db_api
from SNS.db import setup as db_setup
import time



async def on_startup() -> None:
    await db_setup()

app = FastAPI(on_startup=[on_startup])

@app.post(
    "/topic/CreateTopic",
    description="Create a new topic",
    responses={
        200: {"model": topic.TopicCreateSuccess},
        401: {"model": common.UnauthorizedMessage},
        403: {"model": common.ForbiddenMessage},
        500: {"model": common.InternalServerErrorMessage},
    },
    response_model=topic.TopicCreateSuccess,
    status_code=status.HTTP_200_OK,
    response_description="OK",
)

async def create_topic(
    topicc: topic.TopicRequest
):
    try:
        print("create1")
        await myredis.create_topic(topicc)
        await db_api.create_topic(topicc)
        return topic.TopicCreateSuccess(
            **{"message": f"Topic '{topicc.topic_name}' created in set '{topicc.set_name}'", "code": 200, "title": "OK"})
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )



@app.get(
    "/topic/ListTopic",
    description="List topic in specific set",
    responses={
        200: {"model": List},
        404: {"model": common.NotFoundMessage},
        500: {"model": common.InternalServerErrorMessage},
    },
    response_model=List,
    status_code=status.HTTP_200_OK,
    response_description="OK",
)

async def list_topic(
    set_name: str):
  
    try:
        list_topics = await myredis.list_topic(set_name)

        return list_topics

    except Exception as e:
        if hasattr(e, "status_code"):
            raise HTTPException(
                status_code=e.status_code,
                detail=e.detail,
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=str(e)
            )
        

@app.delete(
    "/topic/DeleteQueue",
    description="Delete a queue",
    responses={
        200: {"model": topic.TopicDeleteSuccess},
        401: {"model": common.UnauthorizedMessage},
        403: {"model": common.ForbiddenMessage},
        404: {"model": common.NotFoundMessage}
    },
)

async def delete_topic(
    set_name: str,
    topic_name: str):

    try:
        await myredis.delete_topic(set_name, topic_name)
        
        return {"message": f"Topic '{topic_name}' deleted from set '{set_name}'"}

    except Exception as e:
        if hasattr(e, "status_code"):
            raise HTTPException(
                status_code=e.status_code,
                detail=e.detail,
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=str(e)
            )
        

@app.get(
    "/topic/TopicInfo",
    description="Get topic info",
    responses={
        200: {"model": List},
        404: {"model": common.NotFoundMessage},
        500: {"model": common.InternalServerErrorMessage},
    },
    response_model=List,
    status_code=status.HTTP_200_OK,
    response_description="OK",
)

async def get_topic_info(
    topic_name: str):
  
    try:
        start_time = time.time()

        topic_info = await db_api.get_topic_info(topic_name)
        end_time = time.time()
        execution_time = end_time - start_time

        print("Execution time:", execution_time, "seconds")

        print(topic_info)
        return topic_info

    except Exception as e:
        if hasattr(e, "status_code"):
            raise HTTPException(
                status_code=e.status_code,
                detail=e.detail,
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=str(e)
            )