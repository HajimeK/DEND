# How to run

## Prepare Apache Cassandra as a Docker container

```
$ ＄sudo docker run --name cassandra -p 127.0.0.1:9042:9042 -p 127.0.0.1:9160:9160   -d cassandra
```

## Run Jupyter notebook

Launch Jupyter Notebook and run all the cells.
```
$ jupyter notebook Project_Cassandra.ipynb
```