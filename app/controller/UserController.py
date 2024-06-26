from app.model.user import User
from app.model.tokenblocklist import TokenBlocklist

from app import response, app, db
from flask import request
from flask_jwt_extended import *
from datetime import datetime, timedelta
import uuid

#fungsi register
#mengambil input yaitu username dan password dengan GET kemudian akan disimpan pada database dengan tabel user 
#jika berhasil akan menampilkan pesan 'successfully added user'
def register():
    try:
        username = request.form.get('username')
        password = request.form.get('password')

        users = User(username=username)
        users.setPassword(password)
        db.session.add(users)
        db.session.commit()
        data = singleObject(users)

        return response.success(data, 'successfully added user')

    except Exception as e:
        print(e)

#fungsi single object
#menyimpan nilai id dan username sebagai object 'data'
def singleObject(data):
    data = {
        'id': data.id,
        'username': data.username
    }

    return data


#fungsi login
#mengambil input yaitu username dan password dengan GET
#kemudian akan dicocokkan pada database berdasarkan username dan password yang ada pada database 
#jika berhasil akan membuat access token baru dan refresh token serta menampilkan pesan 'sukses login'
def login():
    try:
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if not user:
            return response.badRequest([], 'Username tidak terdaftar')

        if not user.checkPassword(password):
            return response.badRequest([], 'Kombinasi password salah')

        data = singleObject(user)

        expires = timedelta(days=7)
        expires_refresh = timedelta(days=7)

        acces_token = create_access_token(data, fresh=True, expires_delta=expires)
        refresh_token = create_refresh_token(data, expires_delta=expires_refresh)

        return response.success({
            "data": data,
            "access_token": acces_token,
            "refresh_token": refresh_token,
        }, "Sukses Login!")

    except Exception as e:
        print(e)
        

#fungsi login guest
#mengenerate username dan password secara otomatis yaitu username = "Guest" dan password = "guest" 
#kemudian username dan password tersebut akan disimpan pada database
#jika berhasil akan membuat access token baru dan refresh token serta pesan 'Successfully login as a guest'        
def loginGuest():
    try:
        username = "Guest"+str(uuid.uuid4())
        password = "guest"+str(uuid.uuid4())

        users = User(username=username)
        users.setPassword(password)
        db.session.add(users)
        db.session.commit()

        data = singleObject(users)

        expires = timedelta(days=7)
        expires_refresh = timedelta(days=7)

        acces_token = create_access_token(identity=data, fresh=True, expires_delta=expires)
        refresh_token = create_refresh_token(identity=data, expires_delta=expires_refresh)

        return response.success({
            "access_token": acces_token,
            "refresh_token": refresh_token,
            "user_data": data,
            "username_alias": "Guest"
        }, "Successfully login as a guest")

    except Exception as e:
        print(e)
        
#fungsi modify token
#mengenerate jti yang merupakan JWT ID atau unique identifier dari JWT (JSON Web Token)
#JTI dapat digunakan untuk identifikasi JWT agar JWT yang sudah expired tidak digunakan lagi
#hal tersebut dapat mengatasi user yang sudah logout agar tidak dapat mengakses halaman sebelum melakukan login           
def modify_token(current_user):
    jti = get_jwt()["jti"]
    now = datetime.now()
    user_id=current_user['id']

    db.session.add(TokenBlocklist(jti=jti, created_at=now, type="bearer", user_id=user_id))
    db.session.commit()
    return response.success({}, "Berhasil Logout")

# def logout_guest(current_user):
#     jti = get_jwt()["jti"]
#     now = datetime.now()
#     user_id=current_user['id']
#     username = current_user['username']

#     guest = User.query.filter_by(username=username).first()

#     db.session.add(TokenBlocklist(jti=jti, created_at=now, type="bearer", user_id=user_id))
#     db.session.delete(guest)
#     db.session.commit()
#     return response.success({}, "Berhasil Logout")
