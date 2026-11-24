from fastapi import APIRouter, HTTPException, Depends
from schema.schema import CreateDevice, DeviceSchema
from sqlalchemy.orm import Session
from database.dbModels import User, Device
from deps import get_db, get_current_user
from typing import Annotated

router = APIRouter(
    prefix='/users',
    tags=["Users"],
)

DBdepends = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]

@router.delete('/{user_id}')
def delete_user(current_user : CurrentUser, user_id : int, db : DBdepends):
    if current_user.user_id != user_id : raise HTTPException(404, "Unauthorized")

    user = db.query(User).filter(User.user_id==user_id).first()
    db.delete(user)
    db.commit()
    
    return {
        "code" : 201,
        "message" : "deleted successfully"
    }



@router.post('/{user_id}/device', response_model=DeviceSchema)
def add_device(current_user : CurrentUser, user_id : int, device : CreateDevice, db : DBdepends):
    if not (current_user.user_id == user_id):
        raise HTTPException(404, "Unauthorized")
    
    user = db.query(User).filter(User.user_id == user_id).first()

    new_device = Device(
        device_id=device.device_id,
        user_id=user.user_id,
        device_name=device.device_name
    )
    db.add(new_device)
    db.commit()
    db.refresh(new_device)

    return new_device



@router.get('/{user_id}/devices')
def fetch_devices_for_user(current_user : CurrentUser, user_id : int, db : DBdepends):
    if current_user.user_id != user_id: raise HTTPException(404, "User Not Authorized")

    user : bool = db.query(User).filter(User.user_id==user_id).first() != None
    if user : 
        devices : bool = db.query(Device).filter(Device.user_id == user_id).all()
        if devices == None : 
            return "No device Added yet"
        print(devices)
        return devices
    raise HTTPException(status_code=404, detail="Unrecognized User")



@router.delete('/{user_id}/devices/{device_id}')
def delete_device(current_user : CurrentUser, user_id : int, device_id : str, db : DBdepends):
    print(int(current_user.user_id), user_id)

    #if current_user.user_id != user_id: raise HTTPException(404, "User Not Authorized")

    device = db.query(Device).filter(Device.user_id==user_id and Device.device_id==device_id).first()
    if device == None : raise HTTPException(
        status_code=404, detail="Device Not Found"
    )
    db.delete(device)
    db.commit()
    #db.
    return {
        "code" : 201,
        "message" : "deleted successfully"
    }


