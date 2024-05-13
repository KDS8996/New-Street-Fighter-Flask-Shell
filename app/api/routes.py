import logging
from flask import Blueprint, jsonify, request
from models import Fighter, FighterSchema, db
from helpers import token_required

# Set up basic configuration for logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return jsonify({'yee': 'naw'})

@api.route('/fighters', methods=['POST'])
@token_required
def create_fighter(current_user_token):
    data = request.json
    name = data.get('name')
    origin = data.get('origin')
    special_move = data.get('special_move')

    if not name or not origin:
        return jsonify({'error': 'Name and origin are required'}), 400

    fighter = Fighter(name=name, origin=origin, special_move=special_move)
    db.session.add(fighter)
    db.session.commit()

    fighter_schema = FighterSchema()  # Create an instance of FighterSchema
    response = fighter_schema.dump(fighter)  # Dump the fighter object using the instance
    return jsonify(response), 201

@api.route('/fighters', methods=['GET'])
@token_required
def get_fighters(current_user_token):
    fighters = Fighter.query.all()
    fighters_schema = FighterSchema(many=True)  # Ensure this is defined and imported correctly
    response = fighters_schema.dump(fighters)  # Serialize the list of fighters
    return jsonify(response)

@api.route('/fighters/<string:id>', methods=['GET'])
@token_required
def get_fighter(current_user_token, id):
    fighter = Fighter.query.get_or_404(id)
    fighter_schema = FighterSchema()
    response = fighter_schema.dump(fighter)
    return jsonify(response), 200

@api.route('/fighters/<string:id>', methods=['PUT'])
@token_required
def update_fighter(current_user_token, id):
    fighter = Fighter.query.get_or_404(id)  # Ensure the ID is fetched correctly as a string
    data = request.json

    # Directly update fighter attributes from JSON data, with fallbacks to existing values
    fighter.name = data.get('name', fighter.name)
    fighter.origin = data.get('origin', fighter.origin)
    fighter.special_move = data.get('special_move', fighter.special_move)

    # Commit the changes to the database
    db.session.commit()

    # Serialize the updated fighter object to return as JSON
    fighter_schema = FighterSchema()
    response = fighter_schema.dump(fighter)
    return jsonify(response), 200

@api.route('/fighters/<string:id>', methods=['DELETE'])
@token_required
def delete_fighter(current_user_token, id):
    logging.debug(f"Attempting to delete fighter with ID: {id}")

    try:
        fighter = Fighter.query.get_or_404(id)  # Adjust to fetch by string ID
        fighter_schema = FighterSchema()  # Instance to serialize fighter data
        response = fighter_schema.dump(fighter)  # Serialize the fighter data before deleting it

        logging.debug(f"Fighter data to be deleted: {response}")

        db.session.delete(fighter)  # Delete the fighter from the database
        db.session.commit()  # Commit the transaction

        logging.debug(f"Fighter with ID: {id} deleted successfully")
        return jsonify(response), 200

    except Exception as e:
        logging.error(f"Error deleting fighter with ID: {id}, Error: {e}")
        return jsonify({'error': 'Failed to delete fighter', 'message': str(e)}), 500

