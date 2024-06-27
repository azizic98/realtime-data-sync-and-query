from app import connections

def add_suggestion(name):
    command = ['FT.SUGADD','name_autocomplete',name,1]
    connections.redis_client.execute_command(*command)

def delete_suggestion(name):
    command = ['FT.SUGDEL','name_autocomplete',name]
    connections.redis_client.execute_command(*command)

def update_suggestion(old_name,new_name):
    delete_suggestion(old_name)
    add_suggestion(new_name)


