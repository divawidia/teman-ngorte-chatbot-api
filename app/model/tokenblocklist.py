from app import db
from datetime import datetime
from app.model.user import User

#membuat tabel TokenBlocklist pada database
#TokenBlocklist akan berisikan id (id TokenBlocklist), jti, type, user_id, dan create
#JTI adalah bagian dari JSON Web Token yang digunakan untuk mencegah JWT yang sama digunakan kembali
#JTI dapat digunakan untuk melacak siapa yang revoked JWT, atau saat token kedaluwarsa
#maka user yang sudah logout harus login kembali untuk mengakses layanan pada website
class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)
    type = db.Column(db.String(16), nullable=False)
    user_id = db.Column(
        db.ForeignKey('user.id', ondelete='CASCADE'),
        default=lambda: User().id,
        nullable=False,
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
