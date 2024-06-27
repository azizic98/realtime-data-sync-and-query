
from redis.commands.search.indexDefinition import IndexDefinition
from app import (connections,
                schemas)



def create_index(redis_client,schema_class):
    
    index_name = schema_class.name
    schema = schema_class.schema
    prefix = schema_class.prefix
    
    try:
        if not check_index_exists(redis_client,index_name):
            redis_client.ft(index_name).create_index(schema, definition=IndexDefinition(prefix=[prefix]))
    except Exception as e:
        print(f"Index creation skipped: {e}")

def check_index_exists(redis_client, index_name):
    try:
        index_info = redis_client.execute_command('FT.INFO', index_name)
        if 'index_name' in index_info:
            print(f"Index '{index_name}' exists.")
            return True
        else:
            print(f"Index '{index_name}' does not exist.")
            return False
    except Exception as e:
        print(f"Error checking index existence: {e}")
        return False


def setup_index():
    print('Creating Index')
    create_index(connections.redis_client,schemas.OutletIndexSchema)
    create_index(connections.redis_client,schemas.ReporterIndexSchema)
    print('Operation Complete.')

