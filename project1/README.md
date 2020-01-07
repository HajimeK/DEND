# Udacity DEND Project 1

## Setting up PostgresSQL

### Pre-requisites.

You have set up docker in your local environment.

### Setup docker container for PostgresSQL

Following will download the PostgreSQL docker container image, and launch the docker container.
```
$ sudo docker run -d --name postgres -e POSTGRES_PASSWORD=DEND postgres:latest
```
In this command, the docker container name postgres is created with the latest PostgreSQL image in the docker hub.


Then you can find the docker containter running PostgresSQL.
```
sudo docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED              STATUS              PORTS               NAMES
4cbb2fdba2aa        postgres:latest     "docker-entrypoint.s…"   About a minute ago   Up About a minute   5432/tcp            postgres
```

To stop the docker container,
```
$ sudo docker stop postgres
```

To start the docker container,
```
$ sudo docker start postgres
```
### Create a database user and add roles

In this project, the database *studentdb* need to be created to manage tables.
Here, we are going to create the database, and default user *student*, in the PostgresSQL running as a docker container.

First launch shell to operate in the docker container, and run PostgreSQL client tool, *psql*.
```
sudo docker exec -it postgres /bin/bash
[sudo] hk のパスワード: 
root@4cbb2fdba2aa:/# which psql
/usr/bin/psql
root@4cbb2fdba2aa:/# /usr/bin/psql -U postgres
psql (12.1 (Debian 12.1-1.pgdg100+1))
Type "help" for help.
```


Create a new user student and assing the same roles as the default postgres user with the client tool.
Adming roles are assigned to the user *student* in the below example.
These will be needed when running DDL scripst.

```
postgres=# CREATE USER student WITH PASSWORD 'student';
postgres=# select * from pg_user;
 usename  | usesysid | usecreatedb | usesuper | userepl | usebypassrls |  passwd  | valuntil | useconfig 
----------+----------+-------------+----------+---------+--------------+----------+----------+-----------
 postgres |       10 | t           | t        | t       | t            | ******** |          | 
 student  |    16384 | f           | f        | f       | f            | ******** |          | 
(2 rows)

postgres=# alter role student with superuser;
ALTER ROLE
postgres=# alter role student with createdb;
ALTER ROLE
postgres=# alter role student with createrole;
ALTER ROLE
postgres=# alter role student with replication;
ALTER ROLE
postgres=# alter role student with bypassrls;
ALTER ROLE
postgres=# \du
                                   List of roles
 Role name |                         Attributes                         | Member of 
-----------+------------------------------------------------------------+-----------
 postgres  | Superuser, Create role, Create DB, Replication, Bypass RLS | {}
 student   | Superuser, Create role, Create DB, Replication, Bypass RLS | {}

```

### Create database 
In this project 

- studentdb
- saprkifydb

are defined as databases. In the PostgreSQL client tool, these are created as below.
The database *sparkifydb* can be dropped and re-created, with the python command provided in the project.
So creating the database *sparkifydb* is not mandatory here.

```
postgres=# CREATE DATABASE studentdb WITH OWNER=student;
postgres=# CREATE DATABASE sparkifydb WITH OWNER=student;
postgres=# \l
                                 List of databases
    Name    |  Owner   | Encoding |  Collate   |   Ctype    |   Access privileges   
------------+----------+----------+------------+------------+-----------------------
 postgres   | postgres | UTF8     | en_US.utf8 | en_US.utf8 | 
 sparkifydb | student  | UTF8     | en_US.utf8 | en_US.utf8 | 
 studentdb  | student  | UTF8     | en_US.utf8 | en_US.utf8 | 
 template0  | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres          +
            |          |          |            |            | postgres=CTc/postgres
 template1  | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres          +
            |          |          |            |            | postgres=CTc/postgres
(5 rows)

```

### Client tools installation (option)

You can operate in the console without lauching the shell in the docker container by installing the client tools as below.

```
$ sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
$ sudo apt update
$ sudo apt install ca-certificates
$ wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
$ sudo apt update
$ apt list --upgradable
$ sudo apt upgrade
$ sudo apt install postgresql-client-12
```

After installed the client tool, we can access DB with the following comment.
```
$ psql -h 172.17.0.2 -p 5432 -U postgres
```
The host ip address 172.17.0.2 can be obtained by 

```
$ docker inspect postgres
```
Find "NetworkSettings"->"IPAddress" in the output.


## Python environment

In this project, python is used to load data and store them into the database.
Here in my project, phthon environment is set up with anaconda 4.8.0 as below.

```
$ conda -V
conda 4.8.0
```

In this project, *psycopg2* and *ipython-sql* need to be additionally installed to access PostgresSQL data from python environment, and see the table entries in the jupyter notebook.
The necessary libraries can be installed with the following command.

```
$ conda install psycopg2
$ conda install -c conda-forge ipython-sql
```

## Running 

### Initialize db

To 
```
$ python create_tables.py
```

### Feed data into DB


```
$ cd python
$ python etl.py
```

### While testing

#### 

```
jupyter notebook etl.ipynb
```

### You can see the 

'''
'''