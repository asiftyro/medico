# Setup on uberspace.de

Ref: <https://lab.uberspace.de/guide_flask/?highlight=flask>

1. create database schema and admin user using phpMYAdmin and mysql_schema.sql
        <https://mysql.uberspace.de/phpmyadmin/>
        ** change db name in line 1 of mysql_schema.sql before executing by phpMyAdmin

2. git clone project to user home ~
        git clone <https://github.com/asiftyro/medico.git>
3. create and activate venv named ENV on python 3.9
        cd medico
        python3.9 -m venv ENV
        source ENV/bin/activate
4. setup packages using pip and requirements.txt

```bash
pip install -r requirements.txt
pip uninstall WeasyPrint
pip install weasyprint==52.5
pip install uWSGI==2.0.21
pip install typer==0.7.0
```

5. setup .env

```bash
cp env.template .env
nano .env
# set the variables
```

6. **first test**:
```python boot.py```

1. create uwsgi.ini

```bash
touch uwsgi.ini
nano uwsgi.ini
```

```bash
[uwsgi]
module = boot:app
pidfile = medico.pid
master = true
processes = 1
http-socket = :1024
chmod-socket = 660
vacuum = true
```

8. **second test**: 
```uwsgi uwsgi.ini```

9.  setup and start daemon, and check status

```bash
touch ~/etc/services.d/medico.ini
nano ~/etc/services.d/medico.ini
```

```bash
[program:medico]
directory=%(ENV_HOME)s/medico
command=%(ENV_HOME)s/medico/ENV/bin/uwsgi uwsgi.ini
```

```bash
supervisorctl reread
supervisorctl update
supervisorctl status
```

```bash
supervisorctl start medico
supervisorctl stop medico
supervisorctl restart medico
```

10. configure a web backend and check status

```bash
uberspace web backend set / --http --port 1024
```

```bash
uberspace web backend list
```


11.  **third test**: from browser
12.  if required, set write permission on dir case-photo, user-avatar, log



Misc:

Web Backend:

Set:
    ```uberspace web backend set / --http --port 1024```
Status:
    ```uberspace web backend list```
Delete:
    ```uberspace web backend del /```


Daemon (supervisord):

Status:
    ```supervisorctl status```

Start:
    ```supervisorctl reread```
    ```supervisorctl update```
    ```supervisorctl start medico```

Stop:
    ```supervisorctl stop medico```

Delete:
    ```rm ~/etc/services.d/medico.ini```
    ```supervisorctl reread```
    ```supervisorctl update```

--------------------------------------------------------------------------------------

## Update

stop app:

```supervisorctl stop medico```

```cd medico``

```git pull```

```nano .env```

```source ENV/bin/activate```

```pip install -r requirements.txt```

```export FLASK_APP=boot```

```flask db upgrade```

test:

```python boot.py```
```uwsgi uwsgi.ini```


finallly:
supervisorctl start medico



--------------------------------------------------------------------------------------


# Setup on pythonanywhere.com

**Following steps consider 'arp' as host username.**

1. Setup mysql database using pythonanywhere mysql console and mysql_schema.sql, and create first user
2. From pythonanywhere bash, in user home ~
```git clone https://github.com/asiftyro/medico.git```

```cd medico```

Make virtual env

```bash
mkvirtualenv venv --python=/usr/bin/python3.9
workon venv
```

Install packages:

```bash
pip install -r requirements.txt
# pip uninstall WeasyPrint
# pip install weasyprint==52.5
pip install typer==0.7.0
```

Setup .env

```bash
cp env.template .env
nano .env
```

In .env define follwoing variables (Delete unused. Used Variables cannot be undefined.)

```bash
# Values: 0 - debug, 1 - production, 2 - statging
PRODUCTION=
APP_NAME=
APP_VER=
# 32 bit random string
SECRET_KEY=
STATIC_DIR_PATH=
LOCAL_TIMEZONE=
APP_HOST=
APP_PORT=
# SQLite for Development
SQLITE_DB_NAME=
# MySQL (Production)
DB_USERNAME=
DB_PASSWORD=
DB_HOST=
DB_NAME=
# MySQL (Staging. i.e. PRODUCTION is 2)
STAGE_DB_USERNAME=
STAGE_DB_PASSWORD=
STAGE_DB_HOST=
STAGE_DB_NAME=
```

From Web panel, create a flask app using default

In Code section of Web panel:
Change Source code:
```/home/arp/mysite```
to
```/home/arp/.virtualenvs/venv```

Click on WSGI configuration file:/var/www/arp_pythonanywhere_com_wsgi.py and change contents as follows

```bash
import sys
import os
from dotenv import load_dotenv

# add your project directory to the sys.path
project_home = '/home/arp/medico'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Load .env
load_dotenv(os.path.join(project_home, '.env'))

# import flask app but need to call it "application" for WSGI to work
from boot import app as application  # noqa
```

In wsgi file editor panel, Press 'Reload arp.pythonanywhere.com' button from top right. [it looks like a refresh button], or from Web panel press 'Reload arp.pythonanywhere.com'. [its the green button and has a refresh icon]

Test from browser.

To view logs, check Log files section of web panel.

