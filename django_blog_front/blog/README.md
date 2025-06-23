
# Enviar Formulario de Contacto a S3 como Correo Interno (Formato MIME)

Este artículo documenta cómo capturar el contenido de un formulario de contacto en un sitio web y enviarlo directamente como un archivo `.eml` (MIME) a un bucket de Amazon S3, simulando un correo interno.

---

## 🧱 Estructura del Formulario

Utilizamos una arquitectura basada en clases reutilizables del tipo `ds-form`:

```html
<form id="contact-form" method="post" action="/api/contact/" class="ds-form">
  <div class="ds-form-entry">
    <label for="name-input" class="ds-form-entry__label">Name:</label>
    <input id="name-input" name="name" type="text" class="ds-input" />
  </div>
  <div class="ds-form-entry">
    <label for="email-input" class="ds-form-entry__label">Email:</label>
    <input id="email-input" name="email" type="text" class="ds-input" />
  </div>
  <div class="ds-form-entry">
    <label for="message-input" class="ds-form-entry__label">Message:</label>
    <textarea id="message-input" name="comments" class="ds-textarea"></textarea>
  </div>
  <div class="ds-form-buttons">
    <button type="submit" class="ds-primary-button">Enviar</button>
  </div>
</form>
```

---

## 🧩 Backend en Django

### Vista

```python
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from email.message import EmailMessage
import boto3
import uuid
from django.utils.timezone import now
from django.conf import settings

@csrf_exempt
def contact_form_s3(request):
    if request.method == "POST":
        name = request.POST.get("name", "")
        email = request.POST.get("email", "")
        message = request.POST.get("comments", "")

        msg = EmailMessage()
        msg["Subject"] = f"Nuevo contacto de {name}"
        msg["From"] = email
        msg["To"] = "contacto@estebanmartins.com.ar"
        msg.set_content(message)

        s3 = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME,
        )

        filename = f"contact/{now().strftime('%Y-%m-%d_%H%M%S')}_{uuid.uuid4().hex}.eml"

        s3.put_object(
            Bucket="mail-esteban",
            Key=filename,
            Body=msg.as_string(),
            ContentType="message/rfc822"
        )

        return HttpResponse("Mensaje recibido correctamente. ¡Gracias!")
```

---

## 🌐 .env de ejemplo

```env
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=Ohx...
AWS_STORAGE_BUCKET_NAME=mail-esteban
AWS_S3_REGION_NAME=us-east-1
```

---

## ✅ Resultado

- El contenido del formulario se guarda como `.eml` en el bucket `mail-esteban`.
- La respuesta es un `HttpResponse` simple con texto plano.
- No se produce redirección.