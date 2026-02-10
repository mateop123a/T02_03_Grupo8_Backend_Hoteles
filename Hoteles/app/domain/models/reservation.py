from app.db import db

class Reservation(db.Model):
    __tablename__ = "reservations"

    id = db.Column(db.String(36), primary_key=True)  # uuid string

    hotel_id = db.Column(db.String(36), db.ForeignKey("hotels.id"), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)

    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)

    check_in = db.Column(db.String(10), nullable=False)
    check_out = db.Column(db.String(10), nullable=False)

    guests = db.Column(db.Integer, nullable=False)
    nights = db.Column(db.Integer, nullable=False)

    price_per_person_night = db.Column(db.Float, nullable=False)
    total_paid = db.Column(db.Float, nullable=False)
    
    payment_method = db.Column(db.String(30), nullable=False)   # "card", "transfer", "cash"
    payment_status = db.Column(db.String(20), nullable=False, default="paid")  # "paid" / "pending"
