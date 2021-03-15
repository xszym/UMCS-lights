# UMCS-lights

![Pipeline status](https://gitlab.com/xszym/UMCS-lights/badges/development/pipeline.svg)

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
`docker-compose up`


## Migrations
Run migrations when server is running

```docker-compose exec backend python manage.py makemigrations```

```docker-compose exec backend python manage.py migrate```

## Testing
`docker-compose exec backend pytest`
