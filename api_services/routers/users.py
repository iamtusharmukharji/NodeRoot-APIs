from database import Session
from flask import request, json
from datetime import datetime
import models, utils, traceback
from sqlalchemy.orm import joinedload

def device_owner_map(device_id, owner_id, db = Session()):

    db_chk = db.query(models.ActiveUser).filter(models.ActiveUser.owner_id == owner_id, models.ActiveUser.device_id == device_id).first()

    if db_chk == None:
        new_map = models.ActiveUser(
            owner_id = owner_id,
            device_id = device_id,
            created_at = datetime.now()
        )
        db.add(new_map)
        db.commit()
        db.refresh(new_map)
    db.close()
    return

def signup(
        db = Session()
        ):
    try:
        payload = dict(request.get_json())
        db_user_check = db.query(models.Owner).filter(models.Owner.email == payload["email"], models.Owner.contact_number == payload["contact"]).first()

        if db_user_check != None:
            db.close()
            return {"detail":"user already exists"}, 403
        
        new_user = models.Owner(
                                first_name = payload["first_name"],
                                last_name = payload.get("last_name", None),
                                user_name = payload["email"],
                                gender = payload.get("gender",None),
                                email = payload["email"],
                                password = utils.get_hashed_password(payload["password"]),
                                contact_number = payload["contact"],
                                address = payload["address"],
                                created_at = datetime.now()
                                )
        db.add(new_user)
        try:
            db.commit()
            
        except Exception as err:
            traceback.print_exc()
            db.rollback()
            db.close()
            return {"detail":str(err)}, 402
        
        db.refresh(new_user)
        db.close()

        device_owner_map(payload["device_id"], new_user.id)
        
        new_user = new_user._asdict()
        new_user.pop("password")

        return {"detail":"new user created","user_data":new_user}, 201
        

    except Exception as err:
        traceback.print_exc()
        return {"error_detail":str(err)}, 403

def get_user_detail(db= Session()):

    try:
        user_id = request.args.get("user_id")
        db_user = db.query(models.Owner).filter(models.Owner.id == int(user_id)).options(joinedload(models.Owner.devices_owner)).first()
        db.close()
        if db_user == None:
            
            return {"detail":"user not found"}, 404
        data = utils.obj_to_dict(db_user)
        print(data)
        data.pop("password")
        data["active_devices"] = utils.arr_obj_to_dict(data.pop("devices_owner"))
        return {"user_detail":data}, 200


    except Exception as err:
        traceback.print_exc()
        return {"detail":str(err)}, 400   
