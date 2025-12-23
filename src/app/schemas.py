from marshmallow import Schema, fields, validates, ValidationError
from .utils.validators import (
    validate_email,
    validate_phone,
    validate_positive_amount,
)

# Opcionales: para validar valores permitidos
ALLOWED_ROLES = {"admin", "recepcionista", "contador"}
ALLOWED_PAYMENT_METHODS = {"cash", "card", "transfer"}
ALLOWED_ROOM_STATUS = {"available", "occupied", "maintenance"}


class UserCreateSchema(Schema):
    username = fields.Str(required=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    role = fields.Str(required=True)

    @validates("username")
    def _username(self, v, **kwargs):
        if not v or len(v.strip()) < 3:
            raise ValidationError("username mínimo 3 caracteres.")

    @validates("email")
    def _email(self, v, **kwargs):
        if v:
            try:
                validate_email(v)
            except ValueError as e:
                raise ValidationError(str(e))

    @validates("password")
    def _password(self, v, **kwargs):
        if not v or len(v) < 6:
            raise ValidationError("password mínimo 6 caracteres.")

    @validates("role")
    def _role(self, v, **kwargs):
        if v not in ALLOWED_ROLES:
            raise ValidationError("role inválido. Use admin/recepcionista/contador.")


class UserOutSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    email = fields.Str()
    role = fields.Str()
    is_active = fields.Bool()
    created_at = fields.DateTime()


class LoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)


class ClientSchema(Schema):
    id = fields.Int(dump_only=True)
    doc_id = fields.Str(required=True)
    full_name = fields.Str(required=True)
    email = fields.Str(allow_none=True)
    phone = fields.Str(allow_none=True)
    address = fields.Str(allow_none=True)

    @validates("doc_id")
    def _doc_id(self, v, **kwargs):
        if not v or len(v.strip()) < 5:
            raise ValidationError("doc_id inválido (mínimo 5 caracteres).")

    @validates("full_name")
    def _full_name(self, v, **kwargs):
        if not v or len(v.strip()) < 3:
            raise ValidationError("full_name inválido (mínimo 3 caracteres).")

    @validates("email")
    def _email(self, v, **kwargs):
        if v:
            try:
                validate_email(v)
            except ValueError as e:
                raise ValidationError(str(e))

    @validates("phone")
    def _phone(self, v, **kwargs):
        if v:
            try:
                validate_phone(v)
            except ValueError as e:
                raise ValidationError(str(e))


class RoomSchema(Schema):
    id = fields.Int(dump_only=True)
    number = fields.Str(required=True)
    room_type = fields.Str(required=True)
    capacity = fields.Int(required=True)
    price_per_night = fields.Float(required=True)
    status = fields.Str(load_default="available")
    is_active = fields.Bool(load_default=True)

    @validates("number")
    def _number(self, v, **kwargs):
        if not v or len(v.strip()) < 1:
            raise ValidationError("number es requerido.")

    @validates("room_type")
    def _room_type(self, v, **kwargs):
        if not v or len(v.strip()) < 3:
            raise ValidationError("room_type inválido (mínimo 3 caracteres).")

    @validates("capacity")
    def _capacity(self, v, **kwargs):
        if v is None or int(v) < 1:
            raise ValidationError("capacity debe ser >= 1.")

    @validates("price_per_night")
    def _price(self, v, **kwargs):
        try:
            validate_positive_amount(float(v))
        except ValueError as e:
            raise ValidationError(str(e))

    @validates("status")
    def _status(self, v, **kwargs):
        if v and v not in ALLOWED_ROOM_STATUS:
            raise ValidationError("status inválido. Use available/occupied/maintenance.")


class ReservationCreateSchema(Schema):
    client_id = fields.Int(required=True)
    room_id = fields.Int(required=True)
    check_in = fields.Date(required=True)
    check_out = fields.Date(required=True)

    @validates("client_id")
    def _client_id(self, v, **kwargs):
        if v is None or int(v) <= 0:
            raise ValidationError("client_id inválido.")

    @validates("room_id")
    def _room_id(self, v, **kwargs):
        if v is None or int(v) <= 0:
            raise ValidationError("room_id inválido.")

    @validates("check_out")
    def _range(self, check_out, **kwargs):
        # La relación check_in < check_out se valida en el Service
        if not check_out:
            raise ValidationError("check_out es requerido.")


class ReservationOutSchema(Schema):
    id = fields.Int()
    code = fields.Str()
    client_id = fields.Int()
    room_id = fields.Int()
    check_in = fields.Date()
    check_out = fields.Date()
    status = fields.Str()
    nights = fields.Int()
    total_amount = fields.Float()
    paid_amount = fields.Float()
    created_at = fields.DateTime()


class PaymentCreateSchema(Schema):
    reservation_id = fields.Int(required=True)
    amount = fields.Float(required=True)
    method = fields.Str(required=True)
    reference = fields.Str(allow_none=True)

    @validates("reservation_id")
    def _reservation_id(self, v, **kwargs):
        if v is None or int(v) <= 0:
            raise ValidationError("reservation_id inválido.")

    @validates("amount")
    def _amount(self, v, **kwargs):
        try:
            validate_positive_amount(float(v))
        except ValueError as e:
            raise ValidationError(str(e))

    @validates("method")
    def _method(self, v, **kwargs):
        if v not in ALLOWED_PAYMENT_METHODS:
            raise ValidationError("method inválido. Use cash/card/transfer.")


class ExpenseCreateSchema(Schema):
    category = fields.Str(required=True)
    amount = fields.Float(required=True)
    description = fields.Str(allow_none=True)

    @validates("category")
    def _category(self, v, **kwargs):
        if not v or len(v.strip()) < 3:
            raise ValidationError("category inválida (mínimo 3 caracteres).")

    @validates("amount")
    def _amount(self, v, **kwargs):
        try:
            validate_positive_amount(float(v))
        except ValueError as e:
            raise ValidationError(str(e))


class InvoiceOutSchema(Schema):
    id = fields.Int()
    reservation_id = fields.Int()
    invoice_number = fields.Str()
    issued_at = fields.DateTime()
    total = fields.Float()


class DateRangeSchema(Schema):
    start = fields.Date(required=True)
    end = fields.Date(required=True)

    @validates("end")
    def _end(self, end, **kwargs):
        if not end:
            raise ValidationError("end requerido.")
