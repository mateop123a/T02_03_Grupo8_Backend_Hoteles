from flask import jsonify, request, session
from . import api_bp
from app.container import reservation_service


@api_bp.get("/reservations")
def list_reservations():
    if session.get("is_admin") is not True:
        return jsonify({"message": "No autorizado"}), 401
    return jsonify(reservation_service.list_reservations())


@api_bp.post("/reservations")
def create_reservation():
    payload = request.get_json(silent=True) or {}

    # ✅ Inyectar identidad desde sesión (NO confiar en el frontend)
    payload["user_id"] = session.get("user_id")
    payload["email"] = session.get("user_email")

    print("PAYLOAD RESERVA:", payload)

    data, err = reservation_service.create_reservation(payload)
    if err:
        print("ERROR RESERVA:", err)
        return jsonify({"message": err}), 400

    return jsonify(data), 201


@api_bp.get("/my-reservations")
def my_reservations():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"message": "No autorizado"}), 401
    return jsonify(reservation_service.list_reservations_by_user_id(int(user_id)))
