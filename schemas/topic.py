from __future__ import annotations

from pydantic import BaseModel, Field


class TopicRequest(BaseModel):
    set_name: str
    topic_name: str
    creator_user_id: str
    access_policy: str
    

class TopicCreateSuccess(BaseModel):
    message: str = Field(..., description="")
    code: int = Field(200, description="Code")
    title: str = Field("OK", description="Title")


class TopicName(BaseModel):
    topic_name: str = Field(..., description="Topic Name")


class TopicInfo(BaseModel):
    set_name: str
    topic_name: str
    


class TopicDeleteSuccess(BaseModel):
    message: str = Field(..., description="")
    code: int = Field(200, description="Code")
    title: str = Field("OK", description="Title")
