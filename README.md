# Medico

**Patient/case management system for Doctors.**

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
yapf==0.32.0
```

## Used theme

Mobified [Start Bootstrap - SB Admin](https://startbootstrap.com/template/sb-admin/) built on bootstrap5

## Dev Notes

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
