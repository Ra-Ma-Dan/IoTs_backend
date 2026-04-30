from pydantic import BaseModel
from datetime import datetime


class CreateUser(BaseModel):
    fullname : str
    username : str
    email : str
    password : str
    number : str

class UserSchema(BaseModel):
    user_id : int
    fullname : str
    username : str
    email : str
    number : int
    date_created : datetime

    class Config:
        from_attributes = True

class DeviceSchema(BaseModel):
    user_id : int
    device_id : str
    device_name : str
    date_added : datetime

    class Config:
        from_attributes = True

class CreateDevice(BaseModel):
    device_id : str
    device_name : str

class DataSchema(BaseModel):
    device_id : str

    voltage : float
    current : float
    power : float

class LoginRequest(BaseModel):
    email : str
    password : str

class TokenRequest(BaseModel):
    pass