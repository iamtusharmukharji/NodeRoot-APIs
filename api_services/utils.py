import bcrypt

def arr_obj_to_dict(arr):
    array = []
    for i in arr:
        temp = obj_to_dict(i)
        array.append(temp)
    return array

def obj_to_dict(obj):

    hashMap = {}

    for attr, value in vars(obj).items():
        if attr[0]!="_":
            
            hashMap[attr] = value

    return hashMap

def get_hashed_password(plain_pass):
    salt = b'$2b$12$GXjVGZ5zq/wRKQoL8STH3u'
    plain_pass = plain_pass.encode('utf-8')

    hashed_pass = bcrypt.hashpw(plain_pass, salt)
    return hashed_pass