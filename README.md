# airflow-poc

Very minimal POC demonstrating data transfer from one Postgresql database into
another using Airflow.

Started from: https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html

## Quickstart after having done airflow initial setup

```
docker-compose -f docker-compose.yaml up -d
docker-compose -f docker-compose-dbs.yaml up -d
./create_schemas.psql
```

Go to airflow UI: http://localhost:8080

Navigate to Admin -> Connections

Define postgresql connections for db1 and db2 (our source and target, correspondingly)

Find your DAG through UI. Trigger it manually and see in the UI if it works.

Insert data into db1, e.g.:

```
psql -h localhost -d postgres -U postgres -p 5432 -c "INSERT INTO test SELECT * FROM generate_series(1,1000000);"
```

And observe how, after DAG execution, data gets copied from db1 into db2.

In my machine about 11M rows of super simple data gets transferred in about
20 seconds using the super straightforward bulk transfer in the POC DAG.
