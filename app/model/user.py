from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# class user
# class ini digunakan untuk mendefinisikan model user yang dimana menjadi penghubung antara aplikasi dengan tabel user pada database dalam memproses data user
# pada class ini didefinisikan field id, username, password, created at, dan updated_at pada tabel user
# fungsi setPassword digunakan untuk mengubah bentuk password dari user dalam bentuk ekripsi hash
# fungsi checkPassword digunakan untuk mendekripsi bentuk password dari user yang berupa format hash
class User(db.Model):
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    created_At = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<User {}>'.format(self.name)

    def setPassword(self, password):
        self.password = generate_password_hash(password)
    
    def checkPassword(self, password):
        return check_password_hash(self.password, password)
