# SGM site

TODO DESCRIPTION


## How to use it

```bash
# TODO SET INRUTION TO RUN FOR DEV
```

<br />

## Deployment

The app is provided with a basic configuration to be executed in [Docker](https://www.docker.com/)  and [Gunicorn](https://gunicorn.org/)

[Docker](https://www.docker.com/) execution
---

### Dev
The application can be easily executed in a docker container. The steps:

> Get the code

```bash
$ git clone git@github.com:Esteban108/sgm-site.git
$ cd sgm-site
```

> Start the app in Docker

```bash
$  docker-compose up --build
```

Visit `http://localhost:9990` in your browser. The app should be up & running.

### Prod

> Set your env vars on .env file   
```.env
SECRET_KEY="SECRET_KEY"
PG_NAME=db_name
PG_USER=db_user
PG_PASSWORD=db_pass
PG_HOST=db_host
PG_PORT=5432
CERTBOT_EMAIL=myemail@email.com
FQDN=myserver.com.uy
```
> Set your env on shell
```bash
$ set -a
$ source .my-env
```
> Start the app in Docker
```bash
$  docker-compose up --build --profile prod
```