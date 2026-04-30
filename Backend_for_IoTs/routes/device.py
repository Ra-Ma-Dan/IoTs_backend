from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from sqlalchemy.orm import Session
from database.dbModels import Device, DeviceData, User
from deps import get_db, get_current_user
from schema.schema import DataSchema


router = APIRouter(
    prefix="/devices",
    tags=["devices"]
)
currentUser = Annotated[User, Depends(get_current_user)]

@router.post('/{device_id}/data', response_model=DataSchema)
def add_data_to_device(
    user_id : int, 
    device_id : str, 
    data : DataSchema, 
    user : currentUser,
    db : Session=Depends(get_db)
):
    if user.user_id != user_id: raise HTTPException(404, "Unauthorized")
    device=db.query(Device).filter(Device.user_id==user_id).first()
    if device == None : raise HTTPException(
        status_code=404, detail="Device not Found"
    )

    new_data = DeviceData(
        device_id=device_id,
        voltage=float(data.voltage),
        current=float(data.current),
        power=float(data.power)
    )
    db.add(new_data)
    db.commit()
    db.refresh(new_data)

    return new_data

@router.get('/{device_id}/data', response_model=DataSchema)
def fetch_device_data(
    device_id : str, 
    user : currentUser,
    limit : int = 10, 
    skip : int = 0,
    db : Session=Depends(get_db)
):
    if currentUser.user_id != user.user_id: raise HTTPException(404, "Unauthorized")

    data = db.query(DeviceData).filter(DeviceData.device_id == device_id).offset(skip).limit(limit).all()
    if data is None: return "Data currently Empty"
    return data

@router.delete('/{device_id}')
def delete_device():
    pass

