import os
import sys

assert len(sys.argv) - 1 == 1
user_input = sys.argv[1]

if user_input == 'run':
    os.system("python manage.py runserver")
elif user_input == 'test':
    os.system("python manage.py test")
elif user_input == 'func':
    os.system("python manage.py test functional_tests")
else:
    exit("ERROR: Wrong argument")