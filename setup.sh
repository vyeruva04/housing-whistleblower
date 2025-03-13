#!/bin/bash

echo "Setting up the project..."

# Step 1: Create virtual environment
python3 -m venv venv

# Step 2: Activate virtual environment
source venv/bin/activate

# Step 3: Install dependencies
pip install -r requirements.txt

# Step 4: Copy .env.example to .env (if not exists)
if [ ! -f .env ]; then
    cp .env.example .env
    echo ".env file created. Please update it with your credentials."
fi

# Step 5: Run migrations
python manage.py migrate

# Step 6: Create superuser (optional)
echo "Do you want to create a Django superuser? (y/n)"
read create_superuser
if [ "$create_superuser" == "y" ]; then
    python manage.py createsuperuser
fi

echo "Setup complete. Run 'source venv/bin/activate' and 'python manage.py runserver' to start the project."
