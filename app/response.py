from flask import jsonify, make_response

#memanggil pesan berupa data value (isi data tersebut) dan message (pesan sukses) apabila API sukses untuk dijalankan 
#HTTP status 200 = success
def success(values, message):
    res = {
        'data' : values,
        'message' : message
    }

    return make_response(jsonify(res)), 200

#memanggil pesan berupa data value (isi data tersebut) dan message (pesan error) apabila API menerima informasi yang tidak valid atau tidak sesuai 
#HTTP status 400 = Bad Request
def badRequest(values, message):
    res = {
        'data' : values,
        'message' : message
    }

    return make_response(jsonify(res)), 400
