from redis_om import get_redis_connection

redis_client = get_redis_connection(
    host="redis",  
    port=6379,         
    decode_responses=True
)