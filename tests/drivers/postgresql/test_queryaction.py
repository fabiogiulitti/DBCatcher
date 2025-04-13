import subprocess
import time
import pytest
import psycopg2
import drivers.postgresql.postgresql.queryactionrules as qar
from main.core.treepath import ItemAction, TreePath,make_session_id, references

@pytest.fixture(scope="module")
def postgres_container():
    container_name = "test_postgres_container"
    subprocess.run([
        "docker", "run", "--name", container_name,
        "-e", "POSTGRES_USER=testuser",
        "-e", "POSTGRES_PASSWORD=testpassword",
        "-e", "POSTGRES_DB=testdb",
        "-p", "5433:5432",  
        "-d", "postgres"
    ])

    time.sleep(2)  # Potresti aumentare il tempo in base al tuo sistema

    yield {
        "host": "localhost",
        "port": 5433,
        "user": "testuser",
        "password": "testpassword",
        "dbname": "testdb"
    }

    subprocess.run(["docker", "rm", "-f", container_name])

def test_postgres_connection(postgres_container):
    ctx = {
        "sessionID": 12345,
        "query": "select 1"

    }
    conn = psycopg2.connect(
        host=postgres_container["host"],
        port=postgres_container["port"],
        user=postgres_container["user"],
        password=postgres_container["password"],
        dbname=postgres_container["dbname"]
    )

    references[12345] = {"client": conn}
    queryActions = qar.PSQueryActionDef()
    result = queryActions._executeQuery(ctx)
    assert result._rows == [(1,)]

    conn.close()
