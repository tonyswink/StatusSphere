from flask import Blueprint, request, jsonify
from app import db
from app.models.icons import Icon
from app.auth.decorators import bearer_auth_required

icons_blueprint = Blueprint('icons', __name__)

@icons_blueprint.route('/', methods=['GET', 'POST'])
@bearer_auth_required
def manage_icons():
    if request.method == 'GET':
        icons = Icon.query.all()
        return jsonify([i.serialize() for i in icons])

    elif request.method == 'POST':
        new_icon = request.json
        icon = Icon(**new_icon)
        db.session.add(icon)
        db.session.commit()
        return jsonify(icon.serialize()), 201

@icons_blueprint.route('/<int:icon_id>', methods=['GET', 'DELETE'])
@bearer_auth_required
def specific_icon(icon_id):
    icon = Icon.query.get(icon_id)
    if not icon:
        return jsonify({"message": "No icon found for provided ID"}), 404

    if request.method == 'GET':
        return jsonify(icon.serialize())

    elif request.method == 'DELETE':
        db.session.delete(icon)
        db.session.commit()
        return jsonify({"message": "Icon deleted successfully"})
