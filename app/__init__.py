# memasukan liibrary yang diperlukan
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
import os

# mendefinisikan nama app dari aplikasi flask
app = Flask(__name__)

SWAGGER_URL = '/api/v1/docs'  # URL for exposing Swagger UI (without trailing '/')
# API_URL = 'http://127.0.0.1:5000/swagger.json'  # Our API url (can of course be a local resource)
API_URL = str(os.environ.get("APP_URL", 'http://127.0.0.1:5000'))+'/swagger.json'

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Teman Ngorte API"
    },
    # oauth_config={  # OAuth config. See https://github.com/swagger-api/swagger-ui#oauth2-configuration .
    #    'clientId': "your-client-id",
    #    'clientSecret': "your-client-secret-if-required",
    #    'realm': "your-realms",
    #    'appName': "your-app-name",
    #    'scopeSeparator': " ",
    #    'additionalQueryStringParams': {'test': "hello"}
    # }
)

app.register_blueprint(swaggerui_blueprint)
# mendefinisikan cors (Cross Origin Resource Sharing) pada aplikasi flask
cors = CORS(app)

# mendefinisikan config yang diperlukan pada aplikasi flask 
app.config.from_object(Config)

# mendefinisikan database dari aplikasi flask dengan menggunakan SQLAlchemy
db = SQLAlchemy(app)

# HOST = str(os.environ.get("DB_HOST"))
# DATABASE = str(os.environ.get("DB_DATABASE"))
# USERNAME = str(os.environ.get("DB_USERNAME"))
# PASSWORD = str(os.environ.get("DB_PASSWORD"))
# PORT = str(os.environ.get("DB_PORT"))

# app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://' + USERNAME + ':' + PASSWORD + '@' + HOST + ':' + PORT + '/' + DATABASE + ''
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.config["SQLALCHEMY_RECORD_QUERIES"] = True
# db.init_app(app)
# mendefinisikan Migrate database yang berguna jika ingin membuat/update pada database
migrate = Migrate(app, db)

# mendefinisikan JWTManager pada aplikasi flask yang digunakan untuk membuat jwt (JSON Web Token) untuk menghasilkan token autorisasi
jwt = JWTManager(app)

#impor model user, message dan tokenblocklist
from app.model import user, message, tokenblocklist


# fungsi yang digunakan untuk mengecek apabila user dengan sebuah access token telah melakukan logout
# pengecekan dilakukan dengan mencocokkan jti pada tabel TokenBlocklist
# Apabila jti ditemukan pada tabel TokenBlocklist maka user terdeteksi telah logout
# token akses (access token) yang diblokir tidak akan dapat mengakses website ini lagi
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload["jti"]
    token = db.session.query(tokenblocklist.TokenBlocklist.id).filter_by(jti=jti).scalar()

    return token is not None


#impor routes
from app import routes


#kembali ke halaman awal
if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8090)))
    app.run()