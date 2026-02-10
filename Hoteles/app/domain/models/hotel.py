from app.db import db

class Hotel(db.Model):
    __tablename__ = "hotels"

    id = db.Column(db.String(36), primary_key=True)  # uuid string
    name = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    stars = db.Column(db.Integer, nullable=False)
    price_per_person_night = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.Text, nullable=False)
