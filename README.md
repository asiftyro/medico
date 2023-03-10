# Medico

**Patient/case management system.** 
*(WIP)*

---

## Used packages

```bash
Flask==2.2.2
Flask-Migrate==4.0.0
Flask-SQLAlchemy==3.0.2
python-dotenv==0.21.0
Flask-Login==0.6.2
Flask-WTF==1.0.1
email-validator==1.3.0
Flask-Minify==0.41
Flask-Compress==1.13
pytz==2022.6
Bootstrap-Flask==2.2.0
python-dateutil==2.8.2
Markdown==3.4.1
mysqlclient==2.1.1
flask_weasyprint==1.0.0

# # # Downgrade weasyprint
# pip uninstall weasyprint
# pip install weasyprint==52.5
# # weasyprint install the followiing
# # cairocffi==1.4.0
# # CairoSVG==2.5.2
# # defusedxml==0.7.1
# # WeasyPrint==52.5

# # # Install python formatter 'black'
black==22.12.0
# # black install the followiing
# # mypy-extensions==0.4.3
# # pathspec==0.10.3
# # platformdirs==2.6.2
# # tomli==2.0.1
# # typing_extensions==4.4.0
```

**\* May need downgrade weasyprint to 52.5 (or lower) depending on host setup.**

```weasyprint==52.5```

## Handled Error pages

```bash
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
405 Method Not Allowed
500 Internal Server Error
```

## Used html theme

Modified [Start Bootstrap - SB Admin](https://startbootstrap.com/template/sb-admin/) built on bootstrap v5

## Dev Notes

### To use flask_weasyprint==1.0.0 on Mac

```brew install weasyprint```

### Install mysql-client on macOS

```bash
# 1: install mysql-client by brew
brew install mysql-client

# 2: add path in ~/.zshrc
echo 'export PATH="/usr/local/opt/mysql-client/bin:$PATH"' >> ~/.zshrc

# 3: load  ~/.zshrc
source ~/.zshrc
```

### Process finding and cleanup on macOS

```bash
# find process running at port 8888
lsof -P -i :8888

# or
ps aux | grep 8888

# kill a process matchin a pattern
pkill -f localhost:8888

# or kill process by pid
kill -9 1234
```

### Uninstall all python packages

```pip freeze | xargs pip uninstall -y```

### change directory permissions

Add permissions:

```chmod +rwx file_or_dir_name```

Remove permissions:

```chmod -rwx file_or_dir_name```

See permission:

```ls -l```

Output description:

```bash
-rwxrwxrwx 
drwxrwxrwx 
lrwxrwxrwx
-rw-rwxrwx

[- : file / d : dir / l : link][rwx- : owner][rwx- : group][rwx- : others]

r : read
w : write
x : excute
- : No Permission
```
