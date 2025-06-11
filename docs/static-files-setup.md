# 🧾 Documentación: Manejo de archivos estáticos (Producción)
## 🎯 Objetivo
Servir archivos estáticos (CSS, JS, imágenes) desde Nginx, generados por Django con collectstatic.

# 📁 Estructura y volumen
Django guarda los archivos en STATIC_ROOT → volumen compartido: static_blog_volume

Nginx accede a ese volumen en modo lectura (ro) y los sirve directamente

# ⚙️ Configuración requerida
## 1. settings.py de Django:


```python
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
```
2. Docker Compose:

```yml
services:
  blog-front:
    volumes:
      - static_blog_volume:/app/static/

  nginx:
    volumes:
      - static_blog_volume:/static:ro
```
## 3. Config Nginx (ej: default.conf o default.dev.conf):

```yml
location /static/ {
    alias /static/;
    access_log off;
    expires 30d;
}
```
## 4. Comando obligatorio al construir la imagen Django:
```bash
python manage.py collectstatic --noinput
Este paso copia todos los archivos desde STATICFILES_DIRS al STATIC_ROOT.
```
