The README file includes a summary of the project, how to run the Python scripts, and an explanation of the files in the repository. Comments are used effectively and each function has a docstring.

## Setting up postgre

```
sudo docker run -d --name postgres -e POSTGRES_PASSWORD=DEND postgres:latest
```

Then you can find the docker containter running PostgresSQL.
```
sudo docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED              STATUS              PORTS               NAMES
4cbb2fdba2aa        postgres:latest     "docker-entrypoint.s…"   About a minute ago   Up About a minute   5432/tcp            postgres
```


To stop:
```
sudo docker stop postgres
```

```
sudo docker start postgres
```

```

CREATE USER student WITH PASSWORD student
```