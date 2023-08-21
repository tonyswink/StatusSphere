from flask import Blueprint, request, jsonify
from app import db
from app.models.status import Status
from app.auth.decorators import bearer_auth_required

status_blueprint = Blueprint('status', __name__)

@status_blueprint.route('/', methods=['GET', 'POST'])
@bearer_auth_required
def manage_statuses():
    if request.method == 'GET':
        statuses = Status.query.all()
        return jsonify([s.serialize() for s in statuses])
    
    elif request.method == 'POST':
        new_status = request.json
        if new_status.get('is_current'):
            Status.query.update({Status.is_current: False})
        
        status = Status(**new_status)
        db.session.add(status)
        db.session.commit()
        return jsonify(status.serialize()), 201

@status_blueprint.route('/<int:status_id>', methods=['GET', 'DELETE', 'PUT'])
@bearer_auth_required
def specific_status(status_id):
    status = Status.query.get(status_id)
    if not status:
        return jsonify({"message": "No status found for provided ID"}), 404

    if request.method == 'GET':
        return jsonify(status.serialize())

    elif request.method == 'DELETE':
        db.session.delete(status)
        db.session.commit()
        return jsonify({"message": "Status deleted successfully"})
    
    elif request.method == 'PUT':
        updates = request.json
        if updates.get('is_current'):
            Status.query.update({Status.is_current: False})
            status.is_current = True

        db.session.commit()
        return jsonify(status.serialize())
    
@status_blueprint.route('/current', methods=['GET', 'POST'])
@bearer_auth_required
def current_status():
    status = Status.query.filter_by(is_current=True).first()
    if not status:
        return jsonify({"message": "No current status set"}), 404
    return jsonify(status.serialize())
