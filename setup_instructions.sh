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
mkdir -p templates/registration

# Generate a new SECRET_KEY if needed
echo ""
echo "Generate a new SECRET_KEY for production by running:"
echo "python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'"
echo ""

# Create the Django database
echo "Creating Django database in PostgreSQL..."
echo "Run these commands in PostgreSQL on localhost:"
echo "CREATE DATABASE helmsman_db;"
echo "CREATE USER helmsman_user WITH PASSWORD 'your-password';"
echo "ALTER ROLE helmsman_user SET client_encoding TO 'utf8';"
echo "ALTER ROLE helmsman_user SET default_transaction_isolation TO 'read committed';"
echo "ALTER ROLE helmsman_user SET timezone TO 'UTC';"
echo "GRANT ALL PRIVILEGES ON DATABASE helmsman_db TO helmsman_user;"
echo ""

# Copy login template
echo "Make sure to place login.html in helmsman/templates/registration/"
echo ""

# Run migrations
echo "Running Django migrations..."
python manage.py makemigrations
python manage.py migrate

# Create superuser
echo ""
echo "Create a Django superuser (for local admin access):"
echo "Note: This is separate from SIS authentication"
python manage.py createsuperuser

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo ""
echo "=== Setup Complete ==="
echo "Remember to:"
echo "1. Update .env file with your actual credentials"
echo "2. Ensure SIS database (ribbon2) on 192.168.56.21 allows connections from this server"
echo "3. Users will log in with their PostgreSQL SIS database username/password"
echo "4. Copy login.html to helmsman/templates/registration/ directory"
echo "5. Configure your web server (nginx/apache) to serve the application"
echo ""
echo "To run the development server:"
echo "source /srv/ribbon2helmsman/venv/bin/activate"
echo "cd /srv/ribbon2helmsman/helmsman"
echo "python manage.py runserver 0.0.0.0:8000"
echo ""
echo "Test login at: http://your-server:8000/accounts/login/"
