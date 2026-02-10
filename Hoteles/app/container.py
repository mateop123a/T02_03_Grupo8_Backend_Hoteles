from app.repositories.hotel_repository import HotelRepository
from app.repositories.reservation_repository import ReservationRepository
from app.repositories.user_repository import UserRepository

from app.services.hotel_service import HotelService
from app.services.reservation_service import ReservationService
from app.services.user_auth_service import UserAuthService

hotel_repo = HotelRepository()
reservation_repo = ReservationRepository()
user_repo = UserRepository()

hotel_service = HotelService(hotel_repo)
reservation_service = ReservationService(reservation_repo, hotel_repo)
user_auth_service = UserAuthService(user_repo)
