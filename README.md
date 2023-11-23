TODO:
- fix slow page loding (25s)
-- setup channels, since the issue is not pytube, but django pagination(listView)
- front end

# Usage:

You can use launch script if you are using linux

```sh
./launch
```

or you can install manualy:

```sh
# to install virtual enviroment
python3 -m venv venv

# to activate virtual enviroment
source venv/bin/activate #on linux 
venv/scripts/activate #on windows

# to install dependencies
pip install -r requirements.txt

# create website/website/local_settings.py
echo "DJANGO_SECRET_KEY='thisShouldBeValidDjangoSecretKey'" > website/website/local_settings.py

# you can generate django secret key using
python3 website/manage.py shell -c "from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())"

# to run django server
python3 website/manage.py runserver 
```

to enter the website goto url: http://127.0.0.1:8000



