from sshtunnel import SSHTunnelForwarder
import psycopg2
from dotenv import load_dotenv
import os

# Carrega variáveis do .env
load_dotenv()

# ====== Configurações SSH ======
ssh_host = os.getenv("SSH_HOST")
ssh_port = int(os.getenv("SSH_PORT", 22))
ssh_user = os.getenv("SSH_USER")
ssh_password = os.getenv("SSH_PASSWORD")

# ====== Configurações PostgreSQL ======
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_port = int(os.getenv("DB_PORT", 5432))
db_host = '127.0.0.1'  # via túnel
local_bind_port = 6543

# Porta local livre para bind
local_bind_port = 6543

# ====== Cria túnel SSH ======
with SSHTunnelForwarder(
    (ssh_host, ssh_port),
    ssh_username=ssh_user,
    ssh_password=ssh_password,
    remote_bind_address=('127.0.0.1', db_port),
    local_bind_address=('127.0.0.1', local_bind_port)
) as tunnel:

    print(f"Túnel SSH estabelecido: localhost:{local_bind_port} → {ssh_host}:{db_port}")

    # ====== Conexão PostgreSQL via túnel ======
    try:
        print("Conectando ao banco de dados PostgreSQL via túnel SSH...")

        conn = psycopg2.connect(
            host=db_host,
            port=tunnel.local_bind_port,
            dbname=db_name,
            user=db_user,
            password=db_password
        )
        cursor = conn.cursor()
        print("Conexão PostgreSQL estabelecida.")

        # Executa a query
        query = 'SELECT * FROM project;'
        cursor.execute(query)

        # Obtém os resultados
        rows = cursor.fetchall()
        print("Resultados da consulta:")
        for row in rows:
            print(row)

    except psycopg2.Error as e:
        print(f"Erro ao conectar ou executar a query no PostgreSQL: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
        print("Conexão PostgreSQL encerrada.")

print("Túnel SSH encerrado.")
