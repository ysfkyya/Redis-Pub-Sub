from sqlalchemy import JSON, Column, Integer, MetaData, String, Table, Boolean

METADATA = MetaData()




Topics = Table(
    "topics",
    METADATA,
    Column("id", Integer, nullable=False, index=True, unique=True),
    Column("set_name", String, nullable=False),
    Column("topic_name", String, nullable=False),
    Column("creator_user_id", String, nullable=False),
    Column("access_policy", String, nullable=False)
)