from app import (operations, 
                suggestions,
                utils)

from models import (outlets,reporters)

def handle_event(payload_dict):

    operation = payload_dict['op']
    
    if operation not in ['c','u','d']:
        return

    table = payload_dict['source']['table']

    primary_keys = {
    'tbl_outlets': 'id',
    'tbl_reporters': 'reporter_id'
    }

    primary_key = primary_keys.get(table)

    unique_id,data = utils.extract(payload_dict,primary_key,operation)
    
    if operation == 'c':
        if table == 'tbl_outlets':
            operations.create(
                model_class=outlets.Outlet,
                unique_id=unique_id,
                data=data
            )
            suggestions.add_suggestion(data['name'])

        elif table == 'tbl_reporters':
            operations.create(
                model_class=reporters.Reporter,
                unique_id=unique_id,
                data=data
            )

    elif operation == 'u':

        updated_data,name_dict = utils.get_updated_data(payload_dict)
        
        if table == 'tbl_outlets':
            
            operations.update(
                model_class=outlets.Outlet,
                unique_id=unique_id,
                data = updated_data
            )
            
            if name_dict:
                suggestions.update_suggestion(
                    old_name=name_dict['old_name'],
                    new_name=name_dict['new_name']
                )


        elif table == 'tbl_reporters':
            operations.update(
                model_class=reporters.Reporter,
                unique_id=unique_id,
                data = updated_data
            )
        print('Update Completed.')
    
    elif operation == 'd':
        pass