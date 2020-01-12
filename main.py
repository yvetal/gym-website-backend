from flask import Flask, request, jsonify

import db_handler as dh

app = Flask(__name__)

@app.route("/")
def hello():
    return "Gym backend"
    
@app.route("/drop_all")
def drop_all():
    dh.drop_all()
    return "dropped all"
    
@app.route("/<category>/add", methods=['POST'])
def add_entity(category):
    result = dh.add_to_db(category, request)
    return result
    
@app.route("/<category>", methods=['GET'])
def get_entities(category):
    result=dh.get_entities(category)
    return jsonify(result)
    
@app.route("/<category>/<ide>", methods=['GET'])
def get_entity(category, ide):
    result=dh.get_entity(category, ide)
    return jsonify(result)
    
@app.route("/<category>/<ide>/edit", methods=['POST'])
def edit_entity(category, ide):
    result=dh.edit_entity(category, ide, request)
    return jsonify(result)
    
@app.route("/<category>/<ide>/history", methods=['GET'])
def get_history(category, ide):
    print('FOUND')
    result=dh.get_history(category, ide)
    return jsonify(result)
    
if __name__ == "__main__":
    app.run(host='0.0.0.0')
