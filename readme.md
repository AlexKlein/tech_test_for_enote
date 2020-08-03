# Solution of the eNote tech test

In this project I showed my Python and SQL coding skills.

## Description

This repository consists of:

```
- an ETL process for delivering data from one CSV-files to PostgreSQL DB;
- SQL scripts which create:
    - database schemas;
    - tables;
    - view.
```

## Docker-compose

When you need to start the app with all infrastructure, you have to make this steps:
1. Change environment variables in [YML-file](./project/docker-compose.yml) (now the default values are) 
2. Execute the `docker-compose up -d --build` command - in this step the app will be built, tables will be created in the DB and ETL process will be started.

## Note

You should wait a couple of minutes for the database starts and the ETL process finishes. You can check it with the `docker ps -a` command. Also, when the `etl-app` is going to finish you can check the logs with the `docker logs -f {etl_app CONTAINER ID}` command.

## Check query task

For this point you have to connect to DB and execute the query:
```
select * from data_mart.transction_m_agg;
```
