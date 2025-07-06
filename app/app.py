from flask import Flask, url_for, flash, redirect, render_template, abort, request
import boto3
from pprint import pprint
from dotenv import load_dotenv
import os
import boto3

ses = boto3.client('ses', region_name='us-east-1')

def enviar_respuesta(destinatario, asunto_original, mensaje, mensaje_original, remitente="info@estebanmartins.com.ar"):
    respuesta_con_historial = (
        f"{mensaje}\n\n"
        "----- Mensaje original -----\n"
        f"De: {mensaje_original.get('from', '')}\n"
        f"Fecha: {mensaje_original.get('fecha', '')}\n"
        f"Asunto: {mensaje_original.get('subject', '')}\n\n"
        f"{mensaje_original.get('body', '')}"
    )

    return ses.send_email(
        Source=remitente,
        Destination={
            'ToAddresses': [destinatario],
        },
        Message={
            'Subject': {'Data': f"Re: {asunto_original}", 'Charset': 'UTF-8'},
            'Body': {
                'Text': {'Data': respuesta_con_historial, 'Charset': 'UTF-8'}
            }
        }
    )


load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

app = Flask(__name__)
secret_key = os.getenv('FLASK_SECRET_KEY')
if not secret_key:
    raise RuntimeError("FLASK_SECRET_KEY not set in .env file")
app.secret_key = secret_key

@app.route('/')
def home():
    return render_template("index.html")

# Ver todos los emails
@app.route('/get_emails')
def get_emails():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1') 
    table = dynamodb.Table('email_received')
    response = table.scan()
    items = response['Items']
    # pprint(items)
    return render_template('mails.html', emails=items)
    # return 'ok'

# Ver Email
@app.route('/view_email/<email_id>')
def view_email(email_id):
    print('test\ntest\ntest')
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('email_received')
    response = table.get_item(Key={'id': email_id})
    item = response.get('Item')
    pprint(item)
    if not item:
        abort(404)
    if not item.get('leido'):
        update_response = table.update_item(
            Key={'id': email_id},
            UpdateExpression='SET leido = :val1',
            ExpressionAttributeValues={':val1': True},
            ReturnValues='UPDATED_NEW'
        )
        item['leido'] = update_response['Attributes']['leido']
    return render_template('email_detail.html', email=item)


# Borrar Email
@app.route('/get_emails/<email_id>/delete', methods=['POST'])
def delete_email(email_id):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('email_received')
    # Verificar si el email existe antes de eliminar
    response = table.get_item(Key={'id': email_id})
    item = response.get('Item')
    if not item:
        flash('Correo no encontrado.', 'danger')
        return redirect(url_for('get_emails'))

    # Intentar eliminar
    table.delete_item(Key={'id': email_id})

    flash('Correo eliminado correctamente.', 'success')
    return redirect(url_for('get_emails'))

@app.route('/view_email/<email_id>/reply', methods=['POST'])
def responder_email(email_id):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('email_received')
    response = table.get_item(Key={'id': email_id})
    item = response.get('Item')

    if not item:
        abort(404)

    mensaje_respuesta = request.form['respuesta']
    destinatario = item['from']
    asunto_original = item['subject']

    enviar_respuesta(
        destinatario=destinatario,
        asunto_original=asunto_original,
        mensaje=mensaje_respuesta,
        mensaje_original=item  # Se usa para construir el historial
    )

    flash('Respuesta enviada correctamente.', 'success')
    return redirect(url_for('view_email', email_id=email_id))