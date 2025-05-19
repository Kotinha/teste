from datetime import datetime

from flask import Blueprint, jsonify, request

from ..models import SessionLocal
from ..models.reservation import Reservation
from ..models.room import Room

bp = Blueprint('reservations', __name__, url_prefix='/reservations')


def get_session():
    return SessionLocal()


def parse_date(value):
    return datetime.strptime(value, '%Y-%m-%d').date()


@bp.route('/', methods=['POST'])
def create_reservation():
    session = get_session()
    data = request.get_json()
    check_in = parse_date(data['check_in'])
    check_out = parse_date(data['check_out'])
    room_id = data['room_id']

    # Check availability
    conflicts = session.query(Reservation).filter(
        Reservation.room_id == room_id,
        Reservation.check_out > check_in,
        Reservation.check_in < check_out,
    ).count()
    if conflicts:
        session.close()
        return jsonify({'error': 'Room not available for given dates'}), 400

    reservation = Reservation(
        guest_name=data['guest_name'],
        check_in=check_in,
        check_out=check_out,
        room_id=room_id,
    )
    session.add(reservation)
    session.commit()
    result = dict(
        id=reservation.id,
        guest_name=reservation.guest_name,
        check_in=reservation.check_in.isoformat(),
        check_out=reservation.check_out.isoformat(),
        room_id=reservation.room_id,
    )
    session.close()
    return jsonify(result), 201


@bp.route('/availability', methods=['GET'])
def check_availability():
    session = get_session()
    room_id = int(request.args['room_id'])
    check_in = parse_date(request.args['check_in'])
    check_out = parse_date(request.args['check_out'])

    conflicts = session.query(Reservation).filter(
        Reservation.room_id == room_id,
        Reservation.check_out > check_in,
        Reservation.check_in < check_out,
    ).count()
    session.close()
    return jsonify({'available': conflicts == 0})


@bp.route('/<int:reservation_id>/checkin', methods=['POST'])
def checkin(reservation_id):
    session = get_session()
    reservation = session.get(Reservation, reservation_id)
    if not reservation:
        session.close()
        return jsonify({'error': 'Reservation not found'}), 404
    room = session.get(Room, reservation.room_id)
    room.status = 'occupied'
    session.commit()
    session.close()
    return jsonify({'status': 'checked-in'})


@bp.route('/<int:reservation_id>/checkout', methods=['POST'])
def checkout(reservation_id):
    session = get_session()
    reservation = session.get(Reservation, reservation_id)
    if not reservation:
        session.close()
        return jsonify({'error': 'Reservation not found'}), 404
    room = session.get(Room, reservation.room_id)
    room.status = 'available'
    session.commit()
    session.close()
    return jsonify({'status': 'checked-out'})
