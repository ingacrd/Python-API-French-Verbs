import requests
from models.verb_model import Verb
from database.__init__ import database
from bson.objectid import ObjectId
import app_config as config
import bcrypt
import jwt
from datetime import datetime, timedelta
from flask import jsonify

# THIS IS FOR THE FIRST ENDPOINT
def fetch_verb(verbInformation):
    try:
        verb = verbInformation["verb"]
        external_api_url = 'https://lasalle-frenchverb-api-afpnl.ondigitalocean.app/v1/api/verb'
        response = requests.get(
            external_api_url, 
            headers={
                'token': '278ef2169b144e879aec4f48383dce28e654a009cacf46f8b6c03bbc9a4b9d11'
            }, 
            json={
                'verb': verb
            }
        )

        print(verb)

        if response.status_code == 200:
            print(response.status_code)
            return jsonify({'verb': response.json()})
        else:
            print(response.json())
            return 'error'
    
    except Exception as err:
        print("Error: ", err)

# THIS IS FOR THE SECOND ENDPOINT
def fetch_random_verb(verbInformation):
    try:
        quantity = verbInformation["quantity"]

        external_api_url = 'https://lasalle-frenchverb-api-afpnl.ondigitalocean.app/v1/api/verb/random'
        response = requests.get(
            external_api_url, 
            headers={
                'token': '278ef2169b144e879aec4f48383dce28e654a009cacf46f8b6c03bbc9a4b9d11'
            }, 
            json={
                'quantity': quantity
            }
        )
        print(quantity)
        if response.status_code == 200:
            print(response.status_code)
            return jsonify({'verbs': response.json()})
        else:
            print(response.status_code)
            print(response.json())
            return 'error'
    
    except Exception as err:
        print('Error: ', err)
    
# THIS IS FOR THE THIRD ENDPOINT
def create_favorite_verb(verbInformation, uid):
    try:
        fav_verb = Verb()
        fav_verb.owner = uid
        fav_verb.verb = verbInformation['verb']

        collection = database.dataBase[config.CONST_VERB_COLLECTION]

        if collection.find_one({'verb': fav_verb.verb}):
            return "Duplicate Favorite"
        
        created_favorite = collection.insert_one(fav_verb.__dict__)

        return created_favorite

    except Exception as err:
        print("Error when creating a new favorite verb: ", err)

# THIS IS FOR THE FOURTH ENDPOINT
def get_favorite_verb(verbId):
    try:
        verb_id = ObjectId(verbId)

        collection = database.dataBase[config.CONST_VERB_COLLECTION]

        result = collection.find_one({'_id': verb_id})

        if result:
            result['_id'] = str(result['_id'])
            return jsonify(result)
        else:
            return jsonify({'error': 'Verb not found'}), 404
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400 

# THIS IS FOR THE FIFTH ENDPOINT
def get_all_favorites(userId):
    try:
        collection = database.dataBase[config.CONST_VERB_COLLECTION]

        verbs = collection.find({"owner": userId}, {'_id': 0})

        if not verbs:
            return "No Favorites"

        return list(verbs)

    except Exception as err:
        return jsonify({'error': str(err)}), 400

# THIS IS FOR THE SIXTH ENDPOINT
def delete_favorite_verb(favoriteId):
    try:
        verb_id = ObjectId(favoriteId)

        collection = database.dataBase[config.CONST_VERB_COLLECTION]

        result = collection.delete_one({'_id': verb_id})

        if result.deleted_count > 0:
            return jsonify({'verbs_affected': result.deleted_count})
        else:
            return "Error"
    
    except Exception as err:
        return jsonify({'error': str(err)}), 400