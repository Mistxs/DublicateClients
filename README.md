# DublicateClients
 
>Early build of a script for searching clients in the database who have the same "phone" field (finding duplicate clients). In the future, it will become a mini-application for Tools4Lulz.

User branch keys are required. To obtain a key, a login and password for the account are needed.

Authentication is done through the method https://developers.yclients.com/ru/#tag/Avtorizaciya/operation/%D0%90%D0%B2%D1%82%D0%BE%D1%80%D0%B8%D0%B7%D0%BE%D0%B2%D0%B0%D1%82%D1%8C%20%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D0%BE%D0%B2%D0%B0%D1%82%D0%B5%D0%BB%D1%8F.

The cut-out file config.py contains a variable called headers. To ensure proper functioning of the script, you need to create a similar file in your repository or define the variables **header** and **user_token** in your project:

```python
headers = {
    'Accept': 'application/vnd.yclients.v2+json',
    'Content-Type': 'application/json',
    'Authorization': user_token
}
```