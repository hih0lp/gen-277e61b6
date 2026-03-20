FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python manage.py collectstatic --noinput 2>/dev/null || true
EXPOSE ${PORT:-8000}
CMD python manage.py migrate && python -c "import django,os;os.environ.setdefault('DJANGO_SETTINGS_MODULE','webapp.settings');django.setup();from core.models import User;User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin','admin@test.com','admin')" && gunicorn webapp.wsgi:application --bind 0.0.0.0:${PORT:-8000}
