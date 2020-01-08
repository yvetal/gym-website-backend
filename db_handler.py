import pymongo
import gridfs
import json
from bson.objectid import ObjectId
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["gym_db_test_0"]
fs = gridfs.GridFS(mydb)
#mycol = mydb["customers"]
from bson.json_util import dumps

def add_to_db(category, request):
    print(category)
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
    x = mycol.insert_one(details)
    for x in mycol.find():
        print(x) 
    return 'Success'
    
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
    
def get_entity(category, ide):
    mycol = mydb[category]
    entity=mycol.find( { '_id' : ObjectId(ide) } )[0]
    entity_json = json.loads(dumps(entity))
    return entity_json
    
def edit_entity(category, ide, request):
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
        
    mycol.update_one({ '_id' : ObjectId(ide) }, { "$set": details })
    return 'Success'
