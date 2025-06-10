# nginx-flask-prod 🚀

Docker Compose stack que levanta **todos mis sitios en producción**  
(Python + Nginx + Docker, sin vendor-lock y fácil de clonar).

| Servicio | Tech | Rol | Carpeta |
|----------|------|-----|---------|
| **nginx-proxy** | Nginx 1.27 | Reverse-proxy HTTPS + servir estáticos | [`/nginx`](nginx) |
| **django-api** | Django 4 + DRF | Backend /admin + REST para el blog | [`/django-api`](django-api) |
| **django_blog_front** | Django templates | Frontend público del blog | [`/django_blog_front`](django_blog_front) |
| **flask-app** | Flask 3 | Landing “En construcción” | [`/app`](app) |

> **Nota**: la antigua carpeta `php/` quedó fuera del repositorio (solo vive en mi server).

---

## Cómo arrancar 🍺

```bash
# clonás el repo
git clone https://github.com/hokuto06/nginx-flask-prod.git
cd nginx-flask-prod

# variables (cambia a gusto)
cp .env.example .env

# build & up con perfiles (nginx + todo el stack)
docker compose --profile prod up -d --build
```



| Puerto   | Servicio              | URL en local                                                 |
| -------- | --------------------- | ------------------------------------------------------------ |
| 80 / 443 | Nginx (reverse proxy) | [http://localhost](http://localhost)                         |
| 8000     | django-api (admin)    | [http://localhost:8000/admin/](http://localhost:8000/admin/) |
| 8500     | django\_blog\_front   | [http://localhost:8500](http://localhost:8500)               |
| 5000     | flask-app             | [http://localhost:5000](http://localhost:5000)               |



| Workflow          | Archivo                        | Qué hace                                                   |
| ----------------- | ------------------------------ | ---------------------------------------------------------- |
| **Deploy-to-EC2** | `.github/workflows/deploy.yml` | Build en GitHub, push a ECR y despliegue vía SSH a mi EC2. |


Variables .env más usadas
env
Copiar
DJANGO_SECRET=…
ALLOWED_HOSTS=estebanmartins.com.ar,portfolio.estebanmartins.com.ar,blog.estebanmartins.com.ar
POSTGRES_URL=postgres://user:pass@db:5432/app
Roadmap
 Terminar página Flask → pasar a React.

 Pipeline de tests (pytest + coverage).

 CDN S3 para media estáticos vía CloudFront + WAF (en progreso).

Autor
Esteban Martins – estebanmartins.com.ar
Si algo rompe, abre un issue o sígueme en LinkedIn ✌️

Copiar
