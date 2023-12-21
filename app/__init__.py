from flask import Flask

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'  # Asegúrate de usar una clave segura y única

from app import routes
