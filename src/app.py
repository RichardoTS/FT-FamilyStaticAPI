"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():
    members = jackson_family.get_all_members()
    response_body = {
        "family": members
    }
    return jsonify(response_body), 200

@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    fetch_member = jackson_family.get_member(member_id)
    if fetch_member:
        return jsonify(fetch_member), 200
    else:
        return jsonify("Could not find that member"), 400

@app.route('/member', methods=['POST'])
def create_member():
    sent_first_name = request.json.get("first_name")
    sent_lucky_numbers = request.json.get("lucky_number")
    sent_age = request.json.get("age")

    if not sent_first_name: return jsonify({'status_code': 400})
    if not sent_lucky_numbers: return jsonify({'status_code': 400})
    if not sent_age: return jsonify({'status_code': 400})
    
    new_member = {
            "id": request.json.get('id') if request.json.get("id") is not None else jackson_family._generateId(),
            "first_name": sent_first_name,
            "last_name": jackson_family.last_name,
            "age": sent_age,
            "lucky_number": sent_lucky_numbers
            }
    response = jackson_family.add_member(new_member)

    return jsonify({'status_code': response})

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    
    member_picked = jackson_family.delete_member(member_id)
    if member_picked:
        return jsonify(member_picked), 200
    else:
        return jsonify("Error deleting family member"), 400

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
