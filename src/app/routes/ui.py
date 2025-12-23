from flask import Blueprint, render_template

bp = Blueprint("ui", __name__)

@bp.get("/ui/login")
def login_page():
    return render_template("login.html")

@bp.get("/ui")
def dashboard():
    return render_template("dashboard.html")

@bp.get("/ui/clients")
def clients_page():
    return render_template("clients.html")

@bp.get("/ui/rooms")
def rooms_page():
    return render_template("rooms.html")

@bp.get("/ui/reservations")
def reservations_page():
    return render_template("reservations.html")

@bp.get("/ui/payments")
def payments_page():
    return render_template("payments.html")

@bp.get("/ui/reports")
def reports_page():
    return render_template("reports.html")
