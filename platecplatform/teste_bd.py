import psycopg2

# Parâmetros de conexão com o banco de dados
db_params = {
    "host": "10.187.6.154",
    "database": "platec",
    "user": "platec",
    "password": "platec"
}

# Consulta SQL para buscar dados da tabela
query = "SELECT * FROM equipamentos;"

try:
    # Conectando ao banco de dados
    connection = psycopg2.connect(**db_params)

    # Criando um cursor para executar a consulta
    cursor = connection.cursor()

    # Executando a consulta
    cursor.execute(query)

    # Recuperando os resultados da consulta
    results = cursor.fetchall()

    # Imprimindo os resultados
    for row in results:
        print(row)

except psycopg2.Error as e:
    print("Erro ao conectar ou executar a consulta:", e)
finally:
    # Certificando-se de fechar o cursor e a conexão
    if cursor:
        cursor.close()
    if connection:
        connection.close()