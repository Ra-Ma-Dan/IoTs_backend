from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database.dbModels import User, DeviceData, Device
from deps import get_db, get_current_user
import database.dbModels as dbModels
from routes import device, user, authenticate
from database.db import Base, engine

app = FastAPI(title="IoT Backend!!")

app.include_router(device.router)
app.include_router(user.router)
app.include_router(authenticate.router)

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

@app.get('/me')
def get_me(current_user = Depends(get_current_user)):
    return current_user 

@app.get('/')
def home():
    return {
        "message" : "Fast API Successfully created"
    }

@app.get('/show_user_db')
def show_users_db(db : Session=Depends(get_db)):
    return db.query(User).all()

@app.get('/show_device_db')
def show_devic_db(db : Session=Depends(get_db)):
    return db.query(Device).all()

@app.get('/show_data_db')
def show_data_db(db : Session=Depends(get_db)):
    return db.query(DeviceData).all()


    # print(returned_token.get("access_token"))
    # return returned_token


