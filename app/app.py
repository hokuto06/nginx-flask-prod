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
    print(response)
    #pprint(response)
    #pprint(response['Items'])
    # for mail in response['Items']:
    # #pprint(mail)
    #     if 'for' in mail:
    #         pprint(mail)
    #         print("From: "+mail['from'],"To "+mail['for'] ,"Asunto: "+mail['subject'])
    return 'ok'