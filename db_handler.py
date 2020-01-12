import pymongo
import gridfs
import json
import collections
from bson.objectid import ObjectId
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["gym_db_test_0"]
fs = gridfs.GridFS(mydb)
#mycol = mydb["customers"]
from bson.json_util import dumps

def get_new_id(category):
    print('ID')
    mycol = mydb[category]
    results=mycol.find()
    id_val=1;
    if results.count()>0:
        results=results.sort('id',-1)
        print(results[0])
        id_val=results[0]['id']+1
    print(id_val)
    return str(id_val)
        
def add_to_db(category, request):
    mycol = mydb[category]
    contents_temp = request.form.to_dict()
    details = {}
    for key in contents_temp:
        details[key] = { 'type': 'string', 'value': contents_temp[key] }
    f=request.files.to_dict()
    for key in f:
        content=f[key].read()
        a=fs.put(content)
        b=fs.put(fs.get(a), filename=key)
        details[key] = { 'type': 'file', 'value': b }
    print(details)
    details['id']=get_new_id(category)
    
    x = mycol.insert_one(details)
    add_to_history(category, details)
    
    return str(x.inserted_id)
    
def process_entities(entities):
    new_entities=entities
    for entity in new_entities:
        new_entities[entity]=str(new_entities[entity])
    return new_entities
    
def get_entities(category):
    mycol = mydb[category]
    entities=mycol.find()
    entities_json = json.loads(dumps(entities))
    return entities_json
    
def get_entity(category, id_val):
    mycol = mydb[category]
    entity = mycol.find_one( { 'id' : id_val } )
    entity_json = json.loads(dumps(entity))
    return entity_json
    
def diff_details(details, last_details):
    diff={}
    for key in details:
        if isinstance(details[key], collections.Mapping):
            difference=diff_details(details[key], last_details[key])
            if difference:
                diff[key]=difference
        elif key in details and key in last_details and details[key]!=last_details[key]:
            diff[key] = details[key]
    return diff
    
def add_to_history(category, details):
    id_val=details['id']
    mycol = mydb[category+'_history']
    history = mycol.find( { 'id' : id_val } )
    print(history)
    if history.count()>0:
        mycol.update_one({ 'id' : id_val }, { "$push": {'entries': details }})
    else:
        insdetails={}
        insdetails['id']=id_val
        insdetails['entries']=[details]
        x=mycol.insert_one(insdetails)
        
def drop_all():
    myclient.drop_database('gym_db_test_0')
    
def get_history(category, id_val):
    mycol = mydb[category+'_history']
    entities=mycol.find_one({ 'id' : id_val })
    entities_json = json.loads(dumps(entities))
    return entities_json
    
def edit_entity(category, id_val, request):
    mycol = mydb[category]
    last_details=mycol.find({ 'id' : id_val })[0]
    contents_temp = request.form.to_dict()
    details = last_details
    for key in contents_temp:
        details[key] = { 'type': 'string', 'value': contents_temp[key] }
    f=request.files.to_dict()
    for key in f:
        content=f[key].read()
        a=fs.put(content)
        b=fs.put(fs.get(a), filename=key)
        details[key] = { 'type': 'file', 'value': b }
        
    mycol.update_one({ 'id' : id_val }, { "$set": details })
    add_to_history(category, details)
    return 'Success'
