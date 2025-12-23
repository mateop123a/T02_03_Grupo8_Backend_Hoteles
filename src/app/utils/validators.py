import re
from datetime import date

EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")

def validate_email(value: str) -> None:
    if not value or not EMAIL_RE.match(value):
        raise ValueError("Email inválido.")

def validate_phone(value: str) -> None:
    if value and (len(value) < 7 or len(value) > 20):
        raise ValueError("Teléfono inválido.")

def validate_positive_amount(amount: float) -> None:
    if amount is None or amount <= 0:
        raise ValueError("El monto debe ser mayor que 0.")

def validate_date_range(check_in: date, check_out: date) -> None:
    if not check_in or not check_out:
        raise ValueError("Fechas de check-in y check-out son obligatorias.")
    if check_in >= check_out:
        raise ValueError("Check-in debe ser anterior a check-out.")
