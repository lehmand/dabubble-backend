#!/bin/bash

python manage.py shell <<EOF
import time

print('Lösche alle user aus Datenbank..')
User.objects.all().delete()
time.sleep(1.5)
print('Alle user wurden gelöscht')

EOF