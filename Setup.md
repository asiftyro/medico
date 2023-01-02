# Setup on Uberspace.de

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
