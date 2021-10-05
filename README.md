# UMCS-lights

![Pipeline status](https://gitlab.com/xszym/UMCS-lights/badges/development/pipeline.svg)
[![coverage report](https://gitlab.com/xszym/UMCS-lights/badges/development/coverage.svg)](https://gitlab.com/xszym/UMCS-lights/-/commits/development) 

The building of the Institute of Computer Science at University of Marie Curie Sklodowska is equipped with lights. Each window has a RGB LED panel that can be programmed.

The application will allow users to create scenes and animations that will be displayed on the Institute Building. Additionally, the moderator will be able to manage the displayed animation and the queue of future animations.


## Contributors 

<table>
  <tr>
    <td align="center"><a href="https://github.com/mprostakk"><img src="https://avatars1.githubusercontent.com/u/34036451?s=100&v=4" width="100px;" alt=""/><br /><sub><b>Maciej Prostak</b></sub></a><br /><a href="https://illumination.atlassian.net/browse/IL-38?jql=assignee%20in%20(5ba7f4b7e2a4ab78ab5bd72e)%20AND%20project%20%3D%20IL%20order%20by%20created%20DESC" title="Jira">Jira 👀</a> </td>
    <td align="center"><a href="https://github.com/mMosiur"><img src="https://avatars0.githubusercontent.com/u/39986075?s=100&v=4" width="100px;" alt=""/><br /><sub><b>Mateusz Moruś</b></sub></a><br /><a href="https://illumination.atlassian.net/browse/IL-40?jql=assignee%20in%20(5f80946c8d88b3007551c5a3)%20AND%20project%20%3D%20IL%20order%20by%20created%20DESC" title="Jira">Jira 👀</a></td>
    <td align="center"><a href="https://github.com/dorotajulia"><img src="https://avatars3.githubusercontent.com/u/62723006?s=100&v=4" width="100px;" alt=""/><br /><sub><b>Dorota Zaremba</b></sub></a><br /><a href="https://illumination.atlassian.net/browse/IL-30?jql=assignee%20in%20(5f80946ab61f66006f5ae610)%20AND%20project%20%3D%20IL%20order%20by%20created%20DESC" title="Jira">Jira 👀</a> </td>
    <td align="center"><a href="https://github.com/xszym"><img src="https://avatars2.githubusercontent.com/u/21984800?s=100&v=4" width="100px;" alt=""/><br /><sub><b>Szymon Szostak</b></sub></a><br /><a href="https://illumination.atlassian.net/browse/IL-37?jql=assignee%20in%20(5f8094683fe0760069b54052)%20AND%20project%20%3D%20IL%20order%20by%20created%20DESC" title="Jira">Jira 👀</a></td>
  </tr>
</table>


# Run application
```
docker-compose up
```

## Create superuser
```
docker-compose exec backend python manage.py createsuperuser
```


## Migrations
Run migrations when server is running

```
docker-compose exec backend python manage.py makemigrations
```

```
docker-compose exec backend python manage.py migrate
```

## Testing
```
docker-compose exec backend pytest
```

### Coverage:

```
docker-compose exec backend pytest -p no:warnings --cov=. --cov-report html
```

## Linter
### Flake8 (formatting)

```
docker-compose exec backend flake8 .
```

### Black (formatting)

```
docker-compose exec backend black --check --exclude=migrations .
```

```
docker-compose exec backend black --diff --exclude=migrations .
```

```
docker-compose exec backend black --exclude=migrations .
```

### ISort (sorting)

```
docker-compose exec backend isort . --check-only
```

```
docker-compose exec backend isort . --diff
```

Apply changes

```
docker-compose exec backend isort .
```


## Setup deploy

1. Login to your ssh server (Install docker and docker-compose)

2. Create new user
```
sudo adduser deployer
```

3. Add the user to the Docker group
```
sudo usermod -aG docker deployer
```

4. Log in to created account
```
su deployer
```

5. Generate ssh key
```
ssh-keygen -b 4096
```

6. Add generated public key to authorized keys
```
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
```

7. Copy private key
```
cat ~/.ssh/id_rsa
```

8. Log in to GitLab and go to `Settings > CI / CD > Variables`

9. Click `Add Variable`:

    * Key: `ID_RSA` \
    Value: Paste your SSH private key \
    Type: File \
    Environment Scope: All (default) \
    Protect variable: Checked \
    Mask variable: Unchecked

    * Key: `SERVER_IP` \
    Value: your_server_IP \
    Type: Variable \
    Environment scope: All (default) \
    Protect variable: Checked \
    Mask variable: Checked

    * Key: `SERVER_USER` \
    Value: deployer \
    Type: Variable \
    Environment scope: All (default) \
    Protect variable: Checked \
    Mask variable: Checked

    * Key: `SERVER_SSH_PORT` \
    Value: your_server_SSH_PORT \
    Type: Variable \
    Environment scope: All (default) \
    Protect variable: Checked \
    Mask variable: Checked
    
    
10. Clone this repository
```
git clone https://github.com/xszym/UMCS-lights/
```

11.  To fix issue with `Remote error from secret service: org.freedesktop.DBus.Error.UnknownMethod: No such interface 'org.freedesktop.Secret.Collection' on object at path /org/freedesktop/secrets/collection/login`:
```
sudo apt install gnupg2 pass
```
