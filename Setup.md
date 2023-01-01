# Setup on Uberspace.de

Ref: <https://lab.uberspace.de/guide_flask/?highlight=flask>

1. git clone project to user home ~
2. create and activate venv
3. setup packages using pip and requirements.txt
4. setup uWSGI==2.0.21
5. setup typer==0.7.0
6. setup .env
7. create database schema and admin user
8. update .env with database credential
9. **first test**: python boot.py
10. create uwsgi.ini
11. **second test**: uwsgi uwsgi.ini
12. setup and start daemon
13. configure a web backend
14. **third test**: from browser
15. if required, set write permission on dir case-photo, user-avatar, log
