from flask import Flask, render_template

from .models import init_db, SessionLocal
from .models.room import Room
from .routes.rooms import bp as rooms_bp
from .routes.reservations import bp as reservations_bp


def create_app():
    app = Flask(__name__)
    init_db()
    app.register_blueprint(rooms_bp)
    app.register_blueprint(reservations_bp)

    @app.route('/')
    def home():
        session = SessionLocal()
        rooms = session.query(Room).all()
        session.close()
        return render_template('rooms.html', rooms=rooms)

    @app.route('/reserve')
    def reserve_page():
        return render_template('reservations.html')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
