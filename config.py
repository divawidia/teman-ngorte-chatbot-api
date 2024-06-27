import os
from datetime import datetime, timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

#mendeklarasikan class Config
#mendefinisikan evironment yang digunakan
#HOST yaitu DB_HOST, DATABASE yaitu DB_DATABASE, PASSWORD yaitu DB_PASSWORD, dan PORT yaitu DB_PORT
#mendeklarasikan access_expires (waktu berlaku token habis) dalam waktu 7 hari
#mendeklarasikan JWT SECRET KEY yaitu unique hash (kode unik) yang akan digabungkan dengan header dan payload untuk digunakan pada proses autentikasi user
#menggunakan SQL Alchemy yang merupakan toolkit SQL dan Object Relational Mapper (ORM) yang biasa digunakan untuk Python 
#SQLAlchemy dapat digunakan untuk memuat tabel secara otomatis dari database menggunakan reflection
#reflection adalah istilah dalam SQLAlchemy yang memiliki makna proses membaca database dan membangun metadata berdasarkan informasi tersebut.
class Config(object):
    HOST = str(os.environ.get("DB_HOST"))
    DATABASE = str(os.environ.get("DB_DATABASE"))
    USERNAME = str(os.environ.get("DB_USERNAME"))
    PASSWORD = str(os.environ.get("DB_PASSWORD"))
    PORT = str(os.environ.get("DB_PORT"))
    
    ACCESS_EXPIRES = timedelta(days=7)
    JWT_SECRET_KEY = str(os.environ.get("JWT_SECRET"))
    JWT_ACCESS_TOKEN_EXPIRES = ACCESS_EXPIRES
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + USERNAME + ':' + PASSWORD + '@' + HOST + ':' + PORT + '/' + DATABASE
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://adminTemanNgorte:ekhIODsyODidT935sD64@103.150.196.25:3306/temanNgorte'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    CORS_HEADERS = 'Content-Type'
    
