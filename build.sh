set -o errexit
pip install -r requirements.txt
python manage.py migrate
# Recopilar archivos estáticos
python manage.py collectstatic --no-input