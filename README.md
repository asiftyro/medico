# Medico

Patient/case management system for Doctors

mysql python bootstrap flask python3 sb-admin Flask

## Install mysql-client on macOS

```bash
# 1: install mysql-client by brew
brew install mysql-client

# 2: add path in ~/.zshrc
echo 'export PATH="/usr/local/opt/mysql-client/bin:$PATH"' >> ~/.zshrc

# 3: load  ~/.zshrc
source ~/.zshrc
```

## Process finding and cleanup on macOS

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
