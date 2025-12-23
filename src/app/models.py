# Commit de ajuste final para entrega
from datetime import datetime, date
import uuid
from sqlalchemy import UniqueConstraint, CheckConstraint, Index
from .extensions import db

class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class User(BaseModel):
    __tablename__ = "users"
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # admin/recepcionista/contador
    is_active = db.Column(db.Boolean, default=True, nullable=False)

class Client(BaseModel):
    __tablename__ = "clients"
    doc_id = db.Column(db.String(30), unique=True, nullable=False)  # cédula/pasaporte
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(200), nullable=True)

    reservations = db.relationship("Reservation", back_populates="client", cascade="all,delete-orphan")

class Room(BaseModel):
    __tablename__ = "rooms"
    number = db.Column(db.String(10), unique=True, nullable=False)
    room_type = db.Column(db.String(30), nullable=False)  # simple/doble/suite etc
    capacity = db.Column(db.Integer, nullable=False)
    price_per_night = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="available")  # available/occupied/maintenance
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    __table_args__ = (
        CheckConstraint("capacity >= 1", name="ck_room_capacity_min"),
        CheckConstraint("price_per_night > 0", name="ck_room_price_positive"),
        Index("ix_room_status", "status"),
    )

    reservations = db.relationship("Reservation", back_populates="room", cascade="all,delete-orphan")

class Reservation(BaseModel):
    __tablename__ = "reservations"
    code = db.Column(db.String(20), unique=True, nullable=False, default=lambda: "RSV-" + uuid.uuid4().hex[:10].upper())
    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey("rooms.id"), nullable=False)

    check_in = db.Column(db.Date, nullable=False)
    check_out = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="pending")  # pending/confirmed/cancelled/completed

    nights = db.Column(db.Integer, nullable=False, default=1)
    total_amount = db.Column(db.Float, nullable=False, default=0.0)
    paid_amount = db.Column(db.Float, nullable=False, default=0.0)

    created_by_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    client = db.relationship("Client", back_populates="reservations")
    room = db.relationship("Room", back_populates="reservations")
    payments = db.relationship("Payment", back_populates="reservation", cascade="all,delete-orphan")
    invoice = db.relationship("Invoice", back_populates="reservation", uselist=False, cascade="all,delete-orphan")

    __table_args__ = (
        CheckConstraint("total_amount >= 0", name="ck_res_total_nonneg"),
        CheckConstraint("paid_amount >= 0", name="ck_res_paid_nonneg"),
        Index("ix_res_dates", "check_in", "check_out"),
    )

class Payment(BaseModel):
    __tablename__ = "payments"
    reservation_id = db.Column(db.Integer, db.ForeignKey("reservations.id"), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    method = db.Column(db.String(20), nullable=False)  # cash/card/transfer
    reference = db.Column(db.String(60), nullable=True)
    paid_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    created_by_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    reservation = db.relationship("Reservation", back_populates="payments")

    __table_args__ = (
        CheckConstraint("amount > 0", name="ck_payment_amount_positive"),
        Index("ix_payment_paid_at", "paid_at"),
    )

class Expense(BaseModel):
    __tablename__ = "expenses"
    category = db.Column(db.String(40), nullable=False)  # mantenimiento, servicios, etc.
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=True)
    incurred_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    created_by_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    __table_args__ = (
        CheckConstraint("amount > 0", name="ck_expense_amount_positive"),
        Index("ix_expense_incurred_at", "incurred_at"),
    )

class Invoice(BaseModel):
    __tablename__ = "invoices"
    reservation_id = db.Column(db.Integer, db.ForeignKey("reservations.id"), nullable=False, unique=True)
    invoice_number = db.Column(db.String(30), unique=True, nullable=False)
    issued_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    total = db.Column(db.Float, nullable=False, default=0.0)

    reservation = db.relationship("Reservation", back_populates="invoice")

    __table_args__ = (
        CheckConstraint("total >= 0", name="ck_invoice_total_nonneg"),
    )
