import json

def extract(payload_dict,primary_key,operation):

    if operation in ['c','u']:
        unique_id = payload_dict['after'][primary_key]
        data = payload_dict['after']
    else:
        unique_id = payload_dict['before'][primary_key]
        data = payload_dict['before']

    data.pop(primary_key)

    return unique_id,data

def get_updated_data(payload_dict):

    updated_fields = {}
    name_dict = {}
    before = payload_dict['before']
    after = payload_dict['after']
    
    for field, after_value in after.items():
        before_value = before.get(field)

        if before_value != after_value:
            if field == 'name':
                name_dict['old_name'] = before_value
                name_dict['new_name'] = after_value
                updated_fields[field] = after_value
            else:
                updated_fields[field] = after_value
    
    
    return updated_fields,name_dict

def extract_payload(message):
    # The message key is a JSON string, converting to a dict
    outer_dict = json.loads(list(message.keys())[0])
    
    # The message value is also a JSON string, converting to a dict
    inner_dict = json.loads(list(message.values())[0])
    
    # Extracting the payload from the inner dict
    payload = inner_dict.get('payload', {})
    
    return payload

def escape_special_characters(input_string):
    special_chars = {'/', 
                     ',', 
                     '.', 
                     '<', 
                     '>', 
                     '{', 
                     '}', 
                     '[', 
                     ']', 
                     '"', 
                     "'", 
                     ':', 
                     ';', 
                     '!', 
                     '@', 
                     '#', 
                     '$', 
                     '%', 
                     '^', 
                     '&', 
                     '*', 
                     '(', 
                     ')', 
                     '-', 
                     '+', 
                     '=', 
                     '~'}
    

    escape_char = '\\'
    escaped_list = []

    for char in input_string:
        if char in special_chars:
            escaped_list.append(escape_char + char)
        else:
            escaped_list.append(char)

    return ''.join(escaped_list)