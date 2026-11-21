from sqlalchemy import String, Column, Integer, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from database.db import Base
from datetime import datetime, timezone
from fastapi import APIRouter

router = APIRouter()

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    fullname = Column(String,)
    email = Column(String)
    hased_password = Column(String)
    number = Column(String)
    date_created = Column(DateTime, default=datetime.now(timezone.utc))

    devices = relationship("Device", back_populates='user', cascade="all, delete-orphan")

class Device(Base):
    __tablename__ = 'devices'

    device_id = Column(String, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))

    device_name = Column(String, index=True, unique=True)
    date_added = Column(DateTime, default=datetime.now(timezone.utc))

    user = relationship("User", back_populates="devices")
    data = relationship("DeviceData", back_populates="device", cascade="all, delete-orphan")

class DeviceData(Base):
    __tablename__ = 'device_data'

    device_id = Column(String, ForeignKey('devices.device_id'), primary_key=True)

    voltage = Column(Float)
    current = Column(Float)
    power = Column(Float)
    time_day_sent = Column(DateTime, default=datetime.now(timezone.utc))
    
    device = relationship("Device", back_populates='data')
