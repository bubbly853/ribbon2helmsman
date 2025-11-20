#!/bin/bash
# Setup script for Helmsman Django application

echo "=== Helmsman Django Setup ==="

# Navigate to project root
cd /srv/ribbon2helmsman

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install requirements
echo "Installing Python packages..."
pip install -r requirements.txt

# Navigate to Django project directory
cd helmsman

# Create necessary directories
echo "Creating static and media directories..."
mkdir -p /srv/ribbon2helmsman/static
mkdir -p /srv/ribbon2helmsman/media
mkdir -p staticfiles

# Generate a new SECRET_KEY if needed
echo ""
echo "Generate a new SECRET_KEY for production by running:"
echo "python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'"
echo ""

# Create the Django database
echo "Creating Django database in PostgreSQL..."
echo "Run these commands in PostgreSQL:"
echo "CREATE DATABASE helmsman_db;"
echo "CREATE USER helmsman_user WITH PASSWORD 'your-password';"
echo "ALTER ROLE helmsman_user SET client_encoding TO 'utf8';"
echo "ALTER ROLE helmsman_user SET default_transaction_isolation TO 'read committed';"
echo "ALTER ROLE helmsman_user SET timezone TO 'UTC';"
echo "GRANT ALL PRIVILEGES ON DATABASE helmsman_db TO helmsman_user;"
echo ""

# Run migrations
echo "Running Django migrations..."
python manage.py makemigrations
python manage.py migrate

# Create superuser
echo ""
echo "Create a Django superuser (for local admin access):"
python manage.py createsuperuser

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo ""
echo "=== Setup Complete ==="
echo "Remember to:"
echo "1. Update .env file with your actual credentials"
echo "2. Configure CAS server settings"
echo "3. Set up SIS database user password retrieval in middleware.py"
echo "4. Configure your web server (nginx/apache) to serve the application"
echo ""
echo "To run the development server:"
echo "source /srv/ribbon2helmsman/venv/bin/activate"
echo "cd /srv/ribbon2helmsman/helmsman"
echo "python manage.py runserver 0.0.0.0:8000"
