import psycopg2
import pyodbc

# Configuração da conexão com o MDB
mdb_connection_string = r"DRIVER={Microsoft Access Driver (*.mdb)};DBQ=\\10.187.7.245\C$\smploc\smploc.mdb;UID=Experts;PWD=PPT13.cdm"
mdb_connection = pyodbc.connect(mdb_connection_string)
mdb_cursor = mdb_connection.cursor()

# Configuração da conexão com o PostgreSQL
pg_connection = psycopg2.connect(
    host='10.187.6.154',
    port='5432',
    dbname='platec',
    user='platec',
    password='platec'
)
pg_cursor = pg_connection.cursor()

# Query para extrair os dados do MDB
mdb_query = "SELECT * FROM R_EST_ARRET_FREQUENT"

# Executa a query no MDB
mdb_cursor.execute(mdb_query)

# Loop pelos resultados e inserção no PostgreSQL
for row in mdb_cursor.fetchall():
    # Realize qualquer transformação de dados necessária antes da inserção no PostgreSQL

    # Exemplo de inserção no PostgreSQL
    pg_cursor.execute("INSERT INTO dados (i_arf_numero, i_cda_code234) VALUES (%s, %s)", (row[0], row[1]))

# Commit e fechamento das conexões
pg_connection.commit()
pg_cursor.close()
pg_connection.close()

mdb_cursor.close()
mdb_connection.close()