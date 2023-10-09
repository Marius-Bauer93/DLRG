# DLRG-mail-bot
## Introduction
The **DLRG mail automation service** provides you the code to render and sent multiple emails to different recipients.

## Usage
Below provided are example function calls to...
### Request additional information:
```python
python3 mail_service.py -h
python3 mail_service.py --help
```
### DLRG (default):
```python
python3 mail_service.py -s "someone@example.com" -r "someone-else@example.com" -u "my-user"
python3 mail_service.py --sender "someone@example.com" --reciever "someone-else@example.com" --user "my-user"
```
### General:
```python
python3 mail_service.py -s "someone@example.com" -r "someone-else@example.com" -u "my-user" -ms "example.mail.com" -mp 465
python3 mail_service.py --sender "someone@example.com" --reciever "someone-else@example.com" --user "my-user" --mail-server "example.mail.com" --mail-port 465
```
### Password in plain text:
```python
 python3 mail_service.py -s "someone@example.com" -r "someone-else@example.com" -u "my-user" -ms "example.mail.com" -mp 465 -p "SecretKeyWord"
 python3 mail_service.py --sender "someone@example.com" --reciever "someone-else@example.com" --user "my-user" --mail-server "example.mail.com" --mail-port 465 --password "SecretKeyWord"
```
### Debug mode:
```python
python3 mail_service.py --s "someone@example.com" -r "someone-else@example.com" -u "my-user" -ms "example.mail.com" -mp 465 -v "True"
python3 mail_service.py --sender "someone@example.com" --reciever "someone-else@example.com" --user "my-user" --mail-server "example.mail.com" --mail-port 465 --verbose "True"
```

## Contributor
Persons putting effort into the development of this automation service. In case of any issues with the project feel free to get in contact via GitHub or via email.
|Name|Email|Role|
|----|-----|----|
|Marius|unbelievablebauer@t-online.de|Owner|