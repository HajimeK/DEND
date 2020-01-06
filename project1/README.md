The README file includes a summary of the project, how to run the Python scripts, and an explanation of the files in the repository. Comments are used effectively and each function has a docstring.

## Setting up PostgresSQL

### Setup docker container for PostgresSQL

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

sudo docker exec -it postgres /bin/bash
[sudo] hk のパスワード: 
root@4cbb2fdba2aa:/# which psql
/usr/bin/psql
root@4cbb2fdba2aa:/# /usr/bin/psql -U postgres
psql (12.1 (Debian 12.1-1.pgdg100+1))
Type "help" for help.
```

### Create a database user and add roles

Create a new user student and assing the same roles as the default postgres user.
In this couser user has the password "student".

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

are defined as databases.
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

### Client tools installation

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
psql -h 172.17.0.2 -p 5432 -U postgres
```
The host ip address 172.17.0.2 can be obtained by 

```
$ docker inspect postgres
```
Find "NetworkSettings"->"IPAddress" in the output.


## Python environment

Phthon environment is set up with anaconda 4.8.0 as below.
```
$ conda -V
conda 4.8.0
```
In this project, *psycopg2* need to be additionally installed to access PostgresSQL data from python environment.
The necessary libraries can be installed with the following command.
```
$ conda install psycopg2
Collecting package metadata (current_repodata.json): done
Solving environment: done

## Package Plan ##

  environment location: /home/hk/anaconda3

  added / updated specs:
    - psycopg2


The following packages will be downloaded:

    package                    |            build
    ---------------------------|-----------------
    libpq-11.2                 |       h20c2e04_0         2.0 MB
    psycopg2-2.8.4             |   py37h1ba5d50_0         162 KB
    ------------------------------------------------------------
                                           Total:         2.2 MB

The following NEW packages will be INSTALLED:

  libpq              pkgs/main/linux-64::libpq-11.2-h20c2e04_0
  psycopg2           pkgs/main/linux-64::psycopg2-2.8.4-py37h1ba5d50_0


Proceed ([y]/n)? y


Downloading and Extracting Packages
psycopg2-2.8.4       | 162 KB    | ##################################### | 100% 
libpq-11.2           | 2.0 MB    | ##################################### | 100% 
Preparing transaction: done
Verifying transaction: done
Executing transaction: done

```