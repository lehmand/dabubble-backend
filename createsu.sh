#!/bin/bash

# Script zum Erstellen eines Django Superusers
# Email: daniel@super.com
# Password: password123

echo "Erstelle Django Superuser..."

# Django Management Command ausführen
python manage.py shell << EOF
from django.contrib.auth import get_user_model

User = get_user_model()

# Prüfen ob User bereits existiert
if not User.objects.filter(email='daniel@super.com').exists():
    User.objects.create_superuser(
        email='daniel@super.com',
        password='password123'
    )
    print('✓ Superuser erfolgreich erstellt!')
    print('Email: daniel@super.com')
    print('Password: password123')
else:
    print('! User mit dieser Email existiert bereits.')
    
EOF

echo "Fertig!"