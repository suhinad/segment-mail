# segment-mail
*cd segment-mail*

create *db.py* with

```
SERVER = ''
DATABASE = ''
USERNAME = ''
PASSWORD = ''
```

### create image

```
docker build -t segment-mail .
```

### run container

```
docker run -it -d --restart unless-stopped -p 5000:5000 --name segment-mail segment-mail
```

