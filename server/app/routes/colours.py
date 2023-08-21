from flask import Blueprint, request, jsonify
from app import db
from app.models.colours import Colour
from app.auth.decorators import bearer_auth_required

colours_blueprint = Blueprint('colours', __name__)

@colours_blueprint.route('/', methods=['GET', 'POST'])
@bearer_auth_required
def manage_colours():
    if request.method == 'GET':
        colours = Colour.query.all()
        return jsonify([c.serialize() for c in colours])

    elif request.method == 'POST':
        new_colour = request.json
        colour = Colour(**new_colour)
        db.session.add(colour)
        db.session.commit()
        return jsonify(colour.serialize()), 201

@colours_blueprint.route('/<int:colour_id>', methods=['GET', 'DELETE'])
@bearer_auth_required
def specific_colour(colour_id):
    colour = Colour.query.get(colour_id)
    if not colour:
        return jsonify({"message": "No colour found for provided ID"}), 404

    if request.method == 'GET':
        return jsonify(colour.serialize())

    elif request.method == 'DELETE':
        db.session.delete(colour)
        db.session.commit()
        return jsonify({"message": "Colour deleted successfully"})
