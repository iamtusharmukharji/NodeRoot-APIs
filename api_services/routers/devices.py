from database import Session
from flask import request, json
from datetime import datetime
import models, utils, traceback

def enroll_device(
       db = Session() 
):
    try:
        payload = dict(request.get_json())

        db_device = db.query(models.Device).filter(models.Device.id == payload["serial_number"]).first()

        if db_device != None:
            db.close()
            device = db_device._asdict()
            return {"detail":"device already enrolled","device_detail":device}, 400
        
        new_device = models.Device(
            id = payload["serial_number"],
            model = payload["model"],
            mqtt_topic = payload.get("topic", None),
            created_at = datetime.now()
        )

        try:
            db.add(new_device)
            db.commit()
            db.refresh(new_device)
        except Exception as err:
            traceback.print_exc()
            db.rollback()
            db.close()
            return {"detail":str(err)}, 400
        
        new_device = new_device._asdict()
        db.close()
        return {"detail":"device has been added", "device_detail":new_device}, 201

    except Exception as err:
        traceback.print_exc()

        return {"detail":str(err)}, 400