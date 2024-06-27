from app import (connections,
                suggestions)

from redis import RedisError
from fastapi import HTTPException


def get_by_id(model_class, unique_id):

    key = f"{model_class.Meta.table_name}:{unique_id}"
    data = connections.redis_client.hgetall(key)
    if not data:
        return None
    return model_class(**data)


def create(model_class, unique_id, data):

    table = model_class.Meta.table_name
    
    key = f"{table}:{unique_id}"

    try:
        model_instance = model_class(**data)
        mapping = model_instance.model_dump()

    except Exception as e:
        print(f"Error creating {model_class.__name__}: {e}")
        return None
    
    
    connections.redis_client.hset(key, mapping=mapping)

    if table == 'outlets':
        name = model_instance.name
        suggestions.add_suggestion(name)

    return model_instance
    

def update(model_class,unique_id,data):

    table = model_class.Meta.table_name

    key = f"{table}:{unique_id}"

    
    if not connections.redis_client.exists(key):
        return None
    if data:
        try:
            updated_data = model_class(**data).model_dump(exclude_unset=True)
        except Exception as e:
            print(f"Error updating {model_class.__name__}: {e}")
            return None
        
        connections.redis_client.hset(key, mapping=updated_data)
        return get_by_id(model_class, unique_id)
    else:
        return

def get_duplicates_from_redis(field: str, value: str, index: str):

    try:
        query = f"@{field}:{{{value}}}"
        results = connections.redis_client.ft(index).search(query)
        return results.docs
    except RedisError as e:
        raise HTTPException(status_code=500, detail=f"Redis error: {e}")