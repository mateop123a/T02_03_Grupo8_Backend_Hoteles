from flask import render_template, redirect, request, session
from . import ui_bp
from ..services.auth_service import AuthService
from io import BytesIO
from flask import send_file
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


auth = AuthService()

# -------------------------
# USUARIO (PUBLICO)
# -------------------------
@ui_bp.get("/")
def hotels_public():
    return render_template("hotels/index.html", title="Hoteles")


@ui_bp.get("/reserve/<hotel_id>")
def reserve_page(hotel_id: str):
    if not session.get("user_email"):
        return redirect(f"/login?next=/reserve/{hotel_id}")

    return render_template(
        "hotels/reserve.html",
        title="Reservar",
        hotel_id=hotel_id,
        user_email=session.get("user_email"),
    )


# -------------------------
# ADMIN
# -------------------------
@ui_bp.get("/admin/login")
def admin_login_page():
    return render_template("admin/login.html", title="Admin Login")

@ui_bp.post("/admin/login")
def admin_login_post():
    username = request.form.get("username", "")
    password = request.form.get("password", "")

    if auth.validate_admin(username, password):
        session["is_admin"] = True
        return redirect("/admin")
    return render_template("admin/login.html", title="Admin Login", error="Credenciales incorrectas")

@ui_bp.get("/admin/logout")
def admin_logout():
    session.clear()
    return redirect("/")

@ui_bp.get("/admin")
def admin_dashboard():
    if session.get("is_admin") is not True:
        return redirect("/admin/login")
    return render_template("admin/dashboard.html", title="Panel Admin")


# -------------------------
# ADMIN CRUD PAGES
# -------------------------
@ui_bp.get("/admin/hotels/new")
def admin_new_hotel():
    if session.get("is_admin") is not True:
        return redirect("/admin/login")
    return render_template("admin/hotel_form.html", title="Crear hotel", mode="create", hotel_id="")

@ui_bp.get("/admin/hotels/<hotel_id>/edit")
def admin_edit_hotel(hotel_id: str):
    if session.get("is_admin") is not True:
        return redirect("/admin/login")
    return render_template("admin/hotel_form.html", title="Editar hotel", mode="edit", hotel_id=hotel_id)


# -------------------------
# LEGACY
# -------------------------
@ui_bp.get("/hotels/new")
def legacy_new_redirect():
    return redirect("/admin/hotels/new")

@ui_bp.get("/hotels/<hotel_id>/edit")
def legacy_edit_redirect(hotel_id: str):
    return redirect(f"/admin/hotels/{hotel_id}/edit")


# -------------------------
# AUTH USUARIO
# -------------------------
@ui_bp.get("/login")
def user_login_page():
    next_url = request.args.get("next", "/my-reservations")
    return render_template("auth/login.html", title="Iniciar sesión", next=next_url)

@ui_bp.post("/login")
def user_login_post():
    email = request.form.get("email", "")
    password = request.form.get("password", "")
    next_url = request.form.get("next", "/my-reservations")

    from app.container import user_auth_service, user_repo

    if user_auth_service.validate(email, password):
        email_norm = email.strip().lower()
        u = user_repo.get_by_email(email_norm)

        session["user_email"] = email_norm
        session["user_id"] = u.id if u else None   # ✅ clave para DB

        return redirect(next_url)

    return render_template("auth/login.html", title="Iniciar sesión", error="Credenciales incorrectas", next=next_url)

@ui_bp.get("/register")
def user_register_page():
    next_url = request.args.get("next", "/my-reservations")
    return render_template("auth/register.html", title="Crear cuenta", next=next_url)

@ui_bp.post("/register")
def user_register_post():
    email = request.form.get("email", "")
    password = request.form.get("password", "")
    next_url = request.form.get("next", "/my-reservations")

    from app.container import user_auth_service, user_repo

    err = user_auth_service.register(email, password)
    if err:
        return render_template("auth/register.html", title="Crear cuenta", error=err, next=next_url)

    email_norm = email.strip().lower()
    u = user_repo.get_by_email(email_norm)

    session["user_email"] = email_norm
    session["user_id"] = u.id if u else None       # ✅ clave para DB

    return redirect(next_url)

@ui_bp.get("/logout")
def user_logout():
    session.pop("user_email", None)
    session.pop("user_id", None)
    return redirect("/")

@ui_bp.get("/my-reservations")
def my_reservations_page():
    if not session.get("user_email"):
        return redirect("/login?next=/my-reservations")
    return render_template("hotels/my_reservations.html", title="Mis reservas")

@ui_bp.get("/reservation/<reservation_id>")
def reservation_detail_page(reservation_id: str):
    # ✅ debe estar logueado (usuario o admin)
    if not session.get("user_id") and session.get("is_admin") is not True:
        return redirect(f"/login?next=/reservation/{reservation_id}")

    from app.container import reservation_service, hotel_service

    r, err = reservation_service.get_reservation(reservation_id)
    if err:
        return redirect("/my-reservations")

    # ✅ seguridad: solo dueño o admin
    if session.get("is_admin") is not True:
        if int(r.get("user_id", 0)) != int(session.get("user_id") or 0):
            return redirect("/my-reservations")

    hotel, _ = hotel_service.get_hotel(r["hotel_id"])

    return render_template(
        "hotels/reservation_detail.html",
        title="Comprobante",
        r=r,
        hotel=hotel,
    )

@ui_bp.get("/reservation/<reservation_id>/pdf")
def reservation_pdf(reservation_id: str):
    # ✅ debe estar logueado (usuario o admin)
    if not session.get("user_id") and session.get("is_admin") is not True:
        return redirect(f"/login?next=/reservation/{reservation_id}")

    from app.container import reservation_service, hotel_service

    r, err = reservation_service.get_reservation(reservation_id)
    if err:
        return redirect("/my-reservations")

    # ✅ seguridad: solo dueño o admin
    if session.get("is_admin") is not True:
        if int(r.get("user_id", 0)) != int(session.get("user_id") or 0):
            return redirect("/my-reservations")

    hotel, _ = hotel_service.get_hotel(r["hotel_id"])

    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=letter)

    y = 760
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "Comprobante de Reserva")
    y -= 30

    c.setFont("Helvetica", 11)
    lines = [
        f"ID Reserva: {r['id']}",
        f"Hotel: {hotel.get('name','')} - {hotel.get('city','')}",
        f"Cliente: {r['full_name']} ({r['email']})",
        f"Check-in: {r['check_in']}",
        f"Check-out: {r['check_out']}",
        f"Noches: {r['nights']}",
        f"Huéspedes: {r['guests']}",
        f"Precio: {r['price_per_person_night']} / persona-noche",
        f"Total pagado: {r['total_paid']}",
        f"Método de pago: {r.get('payment_method','')}",
        f"Estado: {r.get('payment_status','')}",
    ]

    for line in lines:
        c.drawString(50, y, line)
        y -= 18

    c.showPage()
    c.save()
    buf.seek(0)

    return send_file(
        buf,
        as_attachment=True,
        download_name=f"comprobante_{reservation_id}.pdf",
        mimetype="application/pdf",
    )
