from database import Base
from sqlalchemy import Column, ForeignKey, FetchedValue
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.dialects.sqlite import INTEGER, VARCHAR, JSON, DATETIME


class Owner(Base):
    __tablename__ = "owner"
    
    id = Column(INTEGER, primary_key = True, index = True)
    user_name = Column(VARCHAR(1024), nullable=False)
    first_name = Column(VARCHAR(128), nullable=False)
    last_name = Column(VARCHAR(128), nullable=True)
    gender = Column(VARCHAR(45))
    email = Column(VARCHAR(128))
    password = Column(VARCHAR(1024))
    contact_number = Column(INTEGER)
    address = Column(VARCHAR(1024))
    created_at = Column(DATETIME)
    updated_at = Column(DATETIME)

    devices_owner = relationship("Device", secondary="active_user", back_populates="owner_devices")

class Device(Base):
    __tablename__ = "device"

    id = Column(VARCHAR(128), primary_key = True, index = True)
    model = Column(VARCHAR(45), nullable=False)
    mqtt_topic = Column(VARCHAR(45), nullable=True)
    last_online = Column(DATETIME)
    created_at = Column(DATETIME)
    updated_at = Column(DATETIME)

    owner_devices = relationship("Owner", secondary="active_user", back_populates="devices_owner")


class ActiveUser(Base):
    __tablename__ = "active_user"

    id = Column(INTEGER, primary_key = True, index = True)
    owner_id = Column(INTEGER, ForeignKey("owner.id"))
    device_id = Column(VARCHAR(128), ForeignKey("device.id"))
    created_at = Column(DATETIME)
