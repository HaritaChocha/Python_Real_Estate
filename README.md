Real Estate WebProject

Tech: Django, Python, HTML, CSS, JS

Steps:

1. Clone the repository
2. Initialize the virtual environment with command: 
    Mac/Linux: source path-to-venv/bin/activate
    Windows: path-to-venv/bin/activate
3. Once the venv is actiavated, install the depandancies with the command: pip install -r requirements.txt
4. Check the depandancy by command: pip list
5. Check if all the systems are working properly. Run python manage.py runserver. The website opens by default on port 8000.
6. If everythings went well, make initial migration:
    - python manage.py makemigrations
    - python manage.py migrate
7. Scripts are present in script folder to initialize the models and other prerequisites.
    - Create super user by running the script createsuperuser.py: python scripts/createsuperuser.py
    - Initialize requisite Data models running the script initializeDatabase.py: python scripts/initializeDatabase.py
8. If everything went well, you will be able to login to admin console and view all the models populated.
    - Admin username: admin
    - Admin password: 12345