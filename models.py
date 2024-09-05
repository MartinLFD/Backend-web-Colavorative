from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String, Date, DateTime, DECIMAL, Text, Enum
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(50), nullable = False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }    

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True )
    first_name = db.Column(db.String(100), nullable = False )
    last_name = db.Column(db.String(100), nullable = False )
    rut = db.Column(db.String(12), unique = True, nullable = False )
    email = db.Column(db.String(100), unique = True, nullable = False )
    password = db.Column(db.String(255), nullable = False )
    role_id = db.Column(db.Integer, ForeignKey('role.id'), nullable = False)
    registration_date = db.Column(DateTime, default = 'CURRENT_TIMESTAMP')
    role = relationship("Role")

    def serialize(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "rut": self.rut,
            "email": self.email,
            "role_id": self.role_id,
            "registration_date": self.registration_date,

        }
    
class Campsite(db.Model):
    __tablename__ = 'campsite'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    provider_id = db.Column(db.Integer, ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    rules = db.Column(db.Text, nullable=True)
    map_url = db.Column(db.String(255), nullable=True)
    image = db.Column(db.String(100), nullable=True)  
        
    provider = relationship("User")
    services = relationship("Service", back_populates="campsite")
    zones = relationship("Site", back_populates="campsite")
    details = relationship("CampsiteDetail", back_populates="campsite")

    def serialize(self):
        return {
            "id": self.id,
            "provider_id": self.provider_id,
            "name": self.name,
            "location": self.location,
            "description": self.description,
            "rules": self.rules,
            "map_url": self.map_url,
            "image": self.image,
        }

class Reservation(db.Model):
    __tablename__ = "reservation"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'), nullable=False)
    campsite_id = db.Column(db.Integer, ForeignKey('campsite.id'), nullable=False)
    site_id = db.Column(db.Integer, ForeignKey('site.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    number_of_people = db.Column(db.Integer, nullable=False)
    reservation_date = db.Column(db.DateTime, default='CURRENT_TIMESTAMP')
    
    user = relationship("User")
    campsite = relationship("Campsite")
    site = relationship("Site")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "campsite_id": self.campsite_id,
            "site": self.site,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "number_of_people": self.number_of_people,
            "reservation_date": self.reservation_date,
        }
    
class Review(db.Model):
    __tablename__ = "review"
    id = db.Column (db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'), nullable=False)
    campsite_id = db.Column(db.Integer, ForeignKey('campsite.id'), nullable=False)
    comment = db.Column(db.Text, nullable=True)
    rating = db.Column (db.Integer, nullable=False)
    date = db.Column(db.DateTime, default='CURRENT_TIMESTAMP')
    
    user = relationship("User")
    campsite = relationship("Campsite")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "campsite_id": self.campsite_id,
            "comment": self.comment,
            "rating": self.rating,
            "date": self.date,
        }
    
class Service_Category(db.Model):
    __tablename__ = "service_category"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }
    
class Service(db.Model):
    __tablename__ = "service"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    campsite_id = db.Column(db.Integer, ForeignKey('campsite.id'), nullable=False)
    category_id = db.Column(db.Integer, ForeignKey('service_category.id'), nullable=False)
    price_by_service = db.Column(db.Integer, nullable = False)

    campsite = relationship("Campsite", back_populates="services")
    category = relationship("ServiceCategory")

    def serialize(self):
        return {
            "id": self.id,
            "campsite_id": self.campsite_id,
            "category_id": self.category_id,
            "price_by_service": self.price_by_service,
        }
    
class Site(db.Model):
    __tablename__ = "site"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    campsite_id = db.Column(db.Integer, ForeignKey('campsite.id'), nullable=False)
    status = db.Column(db.Enum('available', 'unavailable', name='site_status'), default='available')
    
    campsite = relationship("Campsite", back_populates="zones")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "campsite_id": self.campsite_id,
            "status": self.status,
        }
    
class CampsiteDetail(db.Model):
    __tablename__ = "campsitedetail"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    campsite_id = db.Column(db.Integer, ForeignKey('campsite.id'), nullable=False)
    image = db.Column(db.String(100), nullable=False)
    rule = db.Column(db.Text, nullable=True)
    
    campsite = relationship("Campsite", back_populates="details")

    def serialize(self):
        return {
            "id": self.id,
            "campsite_id": self.campsite_id,
            "image": self.image,
            "rule": self.rule,
        }

