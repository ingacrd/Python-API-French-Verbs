from flask import Blueprint, request, jsonify
import json
from helpers.token_validation import validate_token
from controllers.verb_controller import fetch_verb, fetch_random_verb, create_favorite_verb, get_favorite_verb, get_all_favorites, delete_favorite_verb

verb = Blueprint("verb", __name__)

# ENDPOINT 1 - GET A SINGLE VERB
@verb.route("/verbs/", methods=["GET"])
def get_single_verb():
    try:
        token = validate_token()

        data = json.loads(request.data)

        if token == 400:
            return jsonify({'error': "Token is missing in the request, please try again."}), 401
        if token == 401:
            return jsonify({'error': "Invalid authentication token, please login again."}), 403
        
        if 'verb' not in data:
            return jsonify({'error': 'Verb is needed in the request.'}), 400
        
        verb = fetch_verb(data)

        if verb == 'error':
            return jsonify({'error': 'Request to Teacher API was unsuccessful'})
        
        return verb
    
    except Exception:
        return jsonify({'error': 'Something went wrong when trying to fetch the verb.'}), 500
    


# ENDPOINT 2 - GET A RANDOM VERB
@verb.route("/verbs/random/", methods=["GET"])
def get_random_verb():
    try:
        token = validate_token()

        data = json.loads(request.data)

        if token == 400:
            return jsonify({'error': "Token is missing in the request, please try again."}), 401
        if token == 401:
            return jsonify({'error': "Invalid authentication token, please login again."}), 403
        
        if 'quantity' not in data:
            return jsonify({'error': 'Quantity is needed in the request.'}), 400
        
        random_verb = fetch_random_verb(data)

        if random_verb == 'error':
            return jsonify({'error': 'Request to Teacher API was unsuccessful'}), 400
        
        return random_verb
        
    except Exception:
        return jsonify({'error': 'Something went wrong when trying to fetch the verbs'}), 500


# ENDPOINT 3 - ADD A FAVORITE VERB
@verb.route("/verbs/favorites/", methods=["POST"])
def add_favorite():
    try:
        token = validate_token()

        data = json.loads(request.data)

        if token == 400:
            return jsonify({'error': "Token is missing in the request, please try again."}), 401
        if token == 401:
            return jsonify({'error': "Invalid authentication token, please login again."}), 403
        
        if 'verb' not in data:
            return jsonify({'error': 'Verb is needed in the request.'}), 400
        
        uid = token["uid"]

        favorite_verb = create_favorite_verb(data, uid)

        if favorite_verb == "Duplicate Favorite":
            return jsonify({'error': 'This verb is already a favorite.'}), 400
        
        if not favorite_verb.inserted_id:
            return jsonify({'error': 'Something happened when creating a new favorite verb'}), 500
        
        return jsonify({'id': str(favorite_verb.inserted_id)})
        
    except Exception:
        return jsonify({'error': 'Something went wrong when trying to create a new favorite verb.'}), 500
        

# ENDPOINT 4 - GET A SINGLE FAVORITE VERB
@verb.route("/verbs/favorites/<favoriteUid>/", methods=["GET"])
def get_single_favorite(favoriteUid):
    try:
        token = validate_token()

        if token == 400:
            return jsonify({'error': "Token is missing in the request, please try again."}), 401
        if token == 401:
            return jsonify({'error': "Invalid authentication token, please login again."}), 403
        
        favorite = get_favorite_verb(favoriteUid)

        return favorite
    
    except Exception:
        return jsonify({'error': 'Something happened when getting the verb'}), 500

# ENDPOINT 5 - GET ALL FAVORITE VERBS
@verb.route("/verbs/favorites/", methods=["GET"])
def get_favorites():
    try:
        token = validate_token()

        if token == 400:
            return jsonify({'error': "Token is missing in the request, please try again."}), 401
        if token == 401:
            return jsonify({'error': "Invalid authentication token, please login again."}), 403
        
        uid = token["uid"]

        favorites = get_all_favorites(uid)

        if favorites == "No Favorites":
            return jsonify({'error': 'This user has no favorites.'}), 500
        
        return jsonify({'verbs': favorites})

    except Exception:
        return jsonify({'error': 'Something went wrong when fetching all favorite verbs.'}), 500

# ENDPOINT 6 - DELETE A FAVORITE VERB BASED ON ID
@verb.route("/verbs/favorites/<favoriteUid>/", methods=["DELETE"])
def delete_favorite(favoriteUid):
    try:
        token = validate_token()

        if token == 400:
            return jsonify({'error': "Token is missing in the request, please try again."}), 401
        if token == 401:
            return jsonify({'error': "Invalid authentication token, please login again."}), 403

        favorite_id = delete_favorite_verb(favoriteUid)

        if favorite_id == "Error":
            return jsonify({'error': 'Verb not found.'}), 404
        
        return favorite_id

    except Exception:
        return jsonify({'error': 'Something went wrong when trying to delete the favorite.'}), 500



