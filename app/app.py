from flask import Flask, render_template
import boto3
from pprint import pprint



app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/get_mail')
def get_mail():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1') 
    table = dynamodb.Table('email_received')
    response = table.scan()
    items = response['Items']  # Lista de diccionarios
    return render_template('mails.html', tasks=items)