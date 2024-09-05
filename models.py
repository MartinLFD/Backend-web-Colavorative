from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String, Date, DateTime, DECIMAL, Text, Enum
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    rut = db.Column(db.String(12), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(15), nullable=True)  # New field
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    registration_date = db.Column(db.DateTime, default=db.func.current_timestamp())

    role = db.relationship("Role")

    def serialize(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "rut": self.rut,
            "email": self.email,
            "phone": self.phone,
            "role": self.role.serialize(),
            "registration_date": self.registration_date
        }

class Campsite(db.Model):
    __tablename__ = 'campsite'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    provider_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    rules = db.Column(db.Text, nullable=True)
    map_url = db.Column(db.String(255), nullable=True)
    image = db.Column(db.String(100), nullable=True)

    provider = db.relationship("User")
    services = db.relationship("Service", back_populates="campsite")
    zones = db.relationship("Site", back_populates="campsite")
    details = db.relationship("CampsiteDetail", back_populates="campsite")
    prices = db.relationship("Price", back_populates="campsite")

    def serialize(self):
        return {
            "id": self.id,
            "provider": self.provider.serialize(),
            "name": self.name,
            "location": self.location,
            "description": self.description,
            "rules": self.rules,
            "map_url": self.map_url,
            "image": self.image,
            "services": [service.serialize() for service in self.services],
            "zones": [zone.serialize() for zone in self.zones],
            "details": [detail.serialize() for detail in self.details],
            "prices": [price.serialize() for price in self.prices],
        }

class Price(db.Model):
    __tablename__ = 'price'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    campsite_id = db.Column(db.Integer, db.ForeignKey('campsite.id'), nullable=False)
    amount_per_day = db.Column(db.Numeric(10, 2), nullable=False, default=10000)

    campsite = db.relationship("Campsite", back_populates="prices")

    def serialize(self):
        return {
            "id": self.id,
            "campsite_id": self.campsite_id,
            "amount_per_day": float(self.amount_per_day),
        }

class Reservation(db.Model):
    __tablename__ = 'reservation'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    campsite_id = db.Column(db.Integer, db.ForeignKey('campsite.id'), nullable=False)
    site_id = db.Column(db.Integer, db.ForeignKey('site.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    number_of_people = db.Column(db.Integer, nullable=False)
    reservation_date = db.Column(db.DateTime, default=db.func.current_timestamp())

    user = db.relationship("User")
    campsite = db.relationship("Campsite")
    site = db.relationship("Site")

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.serialize(),
            "campsite": self.campsite.serialize(),
            "site": self.site.serialize(),
            "start_date": self.start_date,
            "end_date": self.end_date,
            "number_of_people": self.number_of_people,
            "reservation_date": self.reservation_date,
        }

class Review(db.Model):
    __tablename__ = 'review'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    campsite_id = db.Column(db.Integer, db.ForeignKey('campsite.id'), nullable=False)
    comment = db.Column(db.Text, nullable=True)
    rating = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=db.func.current_timestamp())

    user = db.relationship("User")
    campsite = db.relationship("Campsite")

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.serialize(),
            "campsite": self.campsite.serialize(),
            "comment": self.comment,
            "rating": self.rating,
            "date": self.date,
        }

class ServiceDetail(db.Model):
    __tablename__ = 'service_detail'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": float(self.price),
        }

class Service(db.Model):
    __tablename__ = 'service'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    campsite_id = db.Column(db.Integer, db.ForeignKey('campsite.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service_detail.id'), nullable=False)

    campsite = db.relationship("Campsite", back_populates="services")
    service_detail = db.relationship("ServiceDetail")

    def serialize(self):
        return {
            "id": self.id,
            "campsite": self.campsite.serialize(),
            "service_detail": self.service_detail.serialize(),
        }

class Site(db.Model):
    __tablename__ = 'site'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    campsite_id = db.Column(db.Integer, db.ForeignKey('campsite.id'), nullable=False)
    status = db.Column(db.Enum('available', 'unavailable', name='site_status'), default='available')
    max_of_people = db.Column(db.Integer, nullable=False)

    campsite = db.relationship("Campsite", back_populates="zones")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "campsite_id": self.campsite_id,
            "status": self.status,
            "max_of_people": self.max_of_people,
        }

class CampsiteImage(db.Model):
    __tablename__ = 'campsite_image'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    campsite_id = db.Column(db.Integer, db.ForeignKey('campsite.id'), nullable=False)
    image = db.Column(db.String(100), nullable=False)

    campsite = db.relationship("Campsite")

    def serialize(self):
        return {
            "id": self.id,
            "campsite_id": self.campsite_id,
            "image": self.image,
        }

class CampsiteRule(db.Model):
    __tablename__ = 'campsite_rule'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    campsite_id = db.Column(db.Integer, db.ForeignKey('campsite.id'), nullable=False)
    rule = db.Column(db.Text, nullable=True)

    campsite = db.relationship("Campsite")

    def serialize(self):
        return {
            "id": self.id,
            "campsite_id": self.campsite_id,
            "rule": self.rule,
        }

class ReservationDetail(db.Model):
    __tablename__ = 'reservation_detail'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    reservation_id = db.Column(db.Integer, db.ForeignKey('reservation.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service_detail.id'), nullable=False)

    reservation = db.relationship("Reservation")
    service_detail = db.relationship("ServiceDetail")

    def serialize(self):
        return {
            "id": self.id,
            "reservation": self.reservation.serialize(),
            "service_detail": self.service_detail.serialize(),
        }


