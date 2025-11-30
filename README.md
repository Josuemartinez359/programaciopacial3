# Despliegue en Render (resumen rápido)

Este repositorio contiene una aplicación Django en la carpeta `actividad 1`.

Pasos mínimos para desplegar en Render:

1. En Render, crea un nuevo Web Service. Si tu aplicación Django está dentro de `actividad 1`, pon `Root Directory` = `actividad 1`.

2. Variables de entorno (en Render):
   - SECRET_KEY — string seguro
   - DEBUG = False
   - DATABASE_URL — URL completa de la base de datos Postgres
   - ALLOWED_HOSTS — ejemplo: `my-app.onrender.com,localhost`

3. Build & Start (Render detecta Python):
   - Build command: `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput`
   - Start command: Render usará `Procfile` para lanzar: `web: gunicorn mysite.wsgi:application` (si `Root Directory` = `actividad 1`).

4. Asegúrate de que `requirements.txt` contiene: gunicorn, whitenoise, dj-database-url, psycopg2-binary (ya añadido).

5. Si no quieres usar `Root Directory`, añade un Procfile en la raíz del repo que haga `cd "actividad 1" && gunicorn mysite.wsgi:application`.

6. Recomendaciones de seguridad: activar HTTPS, setear cookies seguras, y no mantener `DEBUG=True` en producción.
