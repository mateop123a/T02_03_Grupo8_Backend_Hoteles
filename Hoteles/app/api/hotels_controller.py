from flask import jsonify, request, session
from . import api_bp
from app.container import hotel_service

def require_admin():
    return session.get("is_admin") is True

@api_bp.get("/hotels")
def list_hotels():
    return jsonify(hotel_service.list_hotels())

@api_bp.get("/hotels/<hotel_id>")
def get_hotel(hotel_id: str):
    data, err = hotel_service.get_hotel(hotel_id)
    if err:
        return jsonify({"message": err}), 404
    return jsonify(data)

@api_bp.post("/hotels")
def create_hotel():
    if not require_admin():
        return jsonify({"message": "No autorizado"}), 401
    payload = request.get_json(silent=True) or {}
    data, err = hotel_service.create_hotel(payload)
    if err:
        return jsonify({"message": err}), 400
    return jsonify(data), 201

@api_bp.put("/hotels/<hotel_id>")
def update_hotel(hotel_id: str):
    if not require_admin():
        return jsonify({"message": "No autorizado"}), 401
    payload = request.get_json(silent=True) or {}
    data, err = hotel_service.update_hotel(hotel_id, payload)
    if err:
        code = 404 if "no encontrado" in err.lower() else 400
        return jsonify({"message": err}), code
    return jsonify(data)

@api_bp.delete("/hotels/<hotel_id>")
def delete_hotel(hotel_id: str):
    if not require_admin():
        return jsonify({"message": "No autorizado"}), 401
    ok, err = hotel_service.delete_hotel(hotel_id)
    if err:
        return jsonify({"message": err}), 404
    return jsonify({"ok": ok})
