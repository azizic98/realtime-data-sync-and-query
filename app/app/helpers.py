from app import schemas



def check_duplicates_reporters(results, field):
    duplicates = []
    for doc in results:
        primary_key = doc.id.split(':')[1]
        duplicate = {
            "reporter_id": primary_key,
            "name": doc.name,
            "outlet_id" : doc.outlet_id,
            field: getattr(doc, field, "")
        }
        duplicates.append(duplicate)

    return schemas.RCheckDuplicatesResponse(duplicates=duplicates)

def check_duplicates_outlets(results, field):
    duplicates = []
    for doc in results:
        primary_key = doc.id.split(':')[1]
        duplicate = {
            "id": primary_key,
            "name": doc.name,
            field: getattr(doc, field, "")
        }
        duplicates.append(duplicate)

    return schemas.OCheckDuplicatesResponse(duplicates=duplicates)