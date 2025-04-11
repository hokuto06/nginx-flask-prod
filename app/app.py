from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "App Flask corriendo con Gunicorn detrás de Nginx - PRODUCCIÓ"
