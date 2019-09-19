from database import db
from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Text, Float
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

# define application model classes

class User(db.Model):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(64), nullable=False)
    last_name = Column(String(64), nullable=False)
    username = Column(String(64), unique=True, nullable=False, index=True)
    password = Column(String(256), nullable=False)
    active = Column(Boolean, default=1)
    email = Column(String(120), unique=True, nullable=False)
    last_login = Column(DateTime)
    login_count = Column(Integer)
    fail_login_count = Column(Integer)
    created_on = Column(DateTime, default=datetime.now, nullable=True)
    changed_on = Column(DateTime, default=datetime.now, nullable=True)
    created_by_fk = Column(Integer)
    changed_by_fk = Column(Integer)

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return int(self.id)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        if self.last_name and self.first_name:
            return '{} {}'.format(
                self.first_name,
                self.last_name
            )


class Message(db.Model):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    text = Column(String(2000), nullable=False)

    def __repr__(self):
        if self.id and self.text:
            return "{} {}".format(
                self.id,
                self.text
            )


class Locations(db.Model):
    """
    Class instance for Store
    """
    __tablename__ = "stores"
    id = Column(Integer, primary_key=True)

    def __repr__(self):
        if self.id:
            return "{}".format(str(id))


class Alerts(db.Model):
    """
    Class instance for Alerts
    """
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.now, nullable=False)
    category = Column(String(50), nullable=False)
    message_id = Column(Integer)
    message_type = Column(String(50), nullable=False)
    message_scope = Column(String(50), nullable=False)
    message_status = Column(String(255), nullable=True)
    description = Column(String(255), nullable=True)
    urgency = Column(String(50), nullable=True)
    severity = Column(String(50), nullable=True)
    status = Column(String(50), nullable=True)
    information_url = Column(String(500), nullable=True)
    sys_mod_count = Column(Integer)
    updated = Column(DateTime, default=datetime.now, nullable=False)
    sender_id = Column(Integer)
    metric_name = Column(String(50), nullable=True)
    certainty = Column(String(50), nullable=True)

    def __repr__(self):
        items = (self.category, self.created, self.message_status, self.description)
        
        if all(items):
            return '{} {} {} {}'.format(
                self.category,
                self.created,
                self.message_status,
                self.description
            )
        return self.id
