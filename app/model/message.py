from app import db
from datetime import datetime
from app.model.user import User

# class message
# class ini digunakan untuk mendefinisikan model message yang dimana menjadi penghubung antara aplikasi dengan tabel message pada database dalam memproses data message
class Message(db.Model):
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    user_msg = db.Column(db.Text(), nullable=False)
    bot_response = db.Column(db.Text(), nullable=False)
    user_timestamp = db.Column(db.DateTime(), default=datetime.utcnow)
    bot_timestamp = db.Column(db.DateTime(), default=datetime.utcnow)
    user_id = db.Column(db.BigInteger, db.ForeignKey(User.id, ondelete='CASCADE'))

    def __repr__(self):
        return '<Message {}>'.format(self.name)