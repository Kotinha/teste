from datetime import datetime

from flask import Blueprint, jsonify, request

from ..models import SessionLocal
from ..models.room import Room
from ..models.reservation import Reservation

bp = Blueprint('rooms', __name__, url_prefix='/rooms')


def get_session():
    return SessionLocal()


def parse_date(value):
    return datetime.strptime(value, "%Y-%m-%d").date()


@bp.route('/', methods=['GET'])
def list_rooms():
    session = get_session()
    rooms = session.query(Room).all()
    data = [
        dict(id=r.id, number=r.number, status=r.status, type=r.type)
        for r in rooms
    ]
    session.close()
    return jsonify(data)


@bp.route('/', methods=['POST'])
def create_room():
    session = get_session()
    data = request.get_json()
    room = Room(
        number=data.get('number'),
        status=data.get('status', 'available'),
        type=data.get('type', 'standard'),
    )
    session.add(room)
    session.commit()
    result = dict(id=room.id, number=room.number, status=room.status, type=room.type)
    session.close()
    return jsonify(result), 201


@bp.route('/available', methods=['GET'])
def available_rooms():
    """Return rooms free for the given dates."""
    check_in = parse_date(request.args['check_in'])
    check_out = parse_date(request.args['check_out'])

    session = get_session()
    conflicts = session.query(Reservation.room_id).filter(
        Reservation.check_out > check_in,
        Reservation.check_in < check_out,
    )
    rooms = (
        session.query(Room)
        .filter(~Room.id.in_(conflicts.subquery()))
        .all()
    )
    data = [
        dict(id=r.id, number=r.number, status=r.status, type=r.type)
        for r in rooms
    ]
    session.close()
    return jsonify(data)


@bp.route('/<int:room_id>', methods=['PUT'])
def update_room(room_id):
    session = get_session()
    room = session.get(Room, room_id)
    if not room:
        session.close()
        return jsonify({'error': 'Room not found'}), 404
    data = request.get_json()
    room.number = data.get('number', room.number)
    room.status = data.get('status', room.status)
    room.type = data.get('type', room.type)
    session.commit()
    result = dict(id=room.id, number=room.number, status=room.status, type=room.type)
    session.close()
    return jsonify(result)
