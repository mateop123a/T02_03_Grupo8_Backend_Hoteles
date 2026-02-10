from app.db import db
from app.domain.models.hotel import Hotel

def seed_hotels():
    if Hotel.query.first():
        return  # ya hay data

    demo = [
        ("Hotel Quito", "Quito", 5, 25.00,
         "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?auto=format&fit=crop&w=1200&q=60"),
        ("Hotel Guayaquil", "Guayaquil", 4, 18.00,
         "https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=1200&q=60"),
        ("Hotel Cuenca", "Cuenca", 3, 12.50,
         "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?auto=format&fit=crop&w=1200&q=60"),
    ]

    for name, city, stars, price, img in demo:
        db.session.add(Hotel(
            id=None,  # si tu modelo no tiene default, pon uuid aquí
            name=name, city=city, stars=stars,
            price_per_person_night=price, image_url=img
        ))

    db.session.commit()
