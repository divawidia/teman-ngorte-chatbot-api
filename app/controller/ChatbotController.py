# mengimport semua library yang dibutuhkan
from app import response, db
from app.model.message import Message
from flask import request
from flask_jwt_extended import *
from datetime import datetime
import time
from googletrans import Translator
from transformers import pipeline
from app.load_model import model, tokenizer

def translate_text(message, src, dest):
    translated_text = Translator().translate(message, src=src, dest=dest).text
    return translated_text

def output(prompt):
    generator = pipeline("text-generation", model=model, tokenizer=tokenizer)
    generated_output = generator(prompt, truncation=True, max_length=256, num_return_sequences=3, return_full_text=False, clean_up_tokenization_spaces=True)
    extracted_output = generated_output[0]['generated_text'].split('."')[0].split(',"')[1]
    return extracted_output

# fungsi get_response
# fungsi ini digunakan untuk menghasilkan output reponse dari chatbot berdasarkan label dengan hasil confidence value tertinggi
# inputan dari fungsi ini berupa pesan chat dari user
def get_response(message):
    translated_message = translate_text(message, 'id', 'en')
    try:
        response = output(translated_message)
    except Exception as e:
        time.sleep(30)
        response = output(translated_message)
    translated_output = translate_text(response, 'en', 'id')
    return translated_output
    

# fungsi post_bot_response_user
# fungsi ini digunakan untuk memasukan data pesan dari user ke dalam database dan menghasilkan output berupa response chatbot terhadap pesan yang dikirim oleh user
# fungsi ini memiliki parameter yaitu user yang sedang login, untuk mendapatkan data id user
def post_bot_response_user(current_user):
    user_text = request.form.get('msg')
    user_timestamp = datetime.now()

    bot_response = get_response(user_text)
    bot_timestamp = datetime.now()

    message = Message(user_msg=user_text, bot_response=bot_response, user_timestamp=user_timestamp, bot_timestamp=bot_timestamp, user_id=current_user['id'])
    db.session.add(message)
    db.session.commit()

    data_message = singleMessage(message)

    return response.success({
        "data_message": data_message,
        "user": current_user
    }, "Success")

# fungsi singleMessage
# fungsi ini digunakan untuk membuat format response json api yang berisi data message dari user dan juga chatbot beserta timestampnya
# fungsi ini memiliki parameter inputan yaitu data pesan dari user
def singleMessage(message):
    data = {
        'id': message.id,
        'user_message': message.user_msg,
        'bot_response': message.bot_response,
        'user_timestamp': message.user_timestamp,
        'bot_timestamp': message.bot_timestamp
    }
    return data

# fungsi formatMessage
# fungsi ini digunakan untuk membuat format response json api dalam bentuk list yang berisi kumpulan/history data message dari user dan juga chatbot beserta timestampnya berdasarkan pada query get data message pada database 
# fungsi ini memiliki parameter inputan yaitu hasil query get data pesan dari user
def formatMessage(data):
    array = []

    for i in data:
        array.append(singleMessage(i))
    return array

# fungsi get_bot_response_user
# fungsi ini digunakan untuk mengambil data pesan dari user dalam database dan menghasilkan output berupa kumpulan response chatbot dan pesan dari user
# fungsi ini memiliki parameter yaitu user yang sedang login, untuk mendapatkan data id user
def get_bot_response_user(current_user):
    message = Message.query.filter_by(user_id=current_user['id'])

    data_message = formatMessage(message)

    return response.success({
        "data_message": data_message,
        "user": current_user
    }, "Success")

# fungsi post_bot_response_guest
# fungsi ini digunakan untuk memasukan data pesan dari guest ke dalam database dan menghasilkan output berupa response chatbot terhadap pesan yang dikirim oleh guest
# fungsi ini memiliki parameter yaitu guest yang sedang login, untuk mendapatkan data id user guest
def post_bot_response_guest(current_user):
    guest_text = request.form.get('msg')
    guest_timestamp = datetime.now()

    bot_response = get_response(guest_text)
    bot_timestamp = datetime.now()

    message = Message(user_msg=guest_text, bot_response=bot_response, user_timestamp=guest_timestamp, bot_timestamp=bot_timestamp, user_id=current_user['id'])
    db.session.add(message)
    db.session.commit()

    data_message = singleMessage(message)

    return response.success({
        "data_message": data_message,
        "user": current_user,
        "username_alias": "Guest"
    }, "Success")

# fungsi get_bot_response_guest
# fungsi ini digunakan untuk mengambil data pesan dari guest dalam database dan menghasilkan output berupa kumpulan response chatbot dan pesan dari guest
# fungsi ini memiliki parameter yaitu guest yang sedang login, untuk mendapatkan data id guest
def get_bot_response_guest(current_user):
    message = Message.query.filter_by(user_id=current_user['id'])

    data_message = formatMessage(message)

    return response.success({
        "data_message": data_message,
        "user": current_user,
        "username_alias": "Guest"
    }, "Success")
